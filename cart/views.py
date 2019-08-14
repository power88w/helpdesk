from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import session
from hardware.models import BlogPost, BlogStats
import braintree
from helpdesk import settings
from . import forms
from django.utils.decorators import method_decorator
from django.views import generic


# Create your views here.

#######################
@login_required(login_url='/login/accounts/login')
def Cart_Fill(request):
    ses = session.objects.filter(user=request.user)
    donation = 0
    for a in ses:
        if a.name.title == "donate":
            donation = a
            break
    count = ses.count()
    total = 0
    if count:
        for blog in ses:
            total += blog.price()
    context = {"sessions": ses, "count": count, "total": total, "donation": donation}
    template = "cart/cart.html"
    return render(request, template, context)


################
@login_required(login_url='/login/accounts/login')
def Item_Up(request, post_id):  # post id is actually session Id
    ses = session.objects.get(id=post_id)
    ses.votes += 1
    ses.save()
    return redirect("/cart/")


################
@login_required(login_url='/login/accounts/login')
def Item_Down(request, post_id):
    ses = session.objects.get(id=post_id)
    if ses.votes > 1:
        ses.votes -= 1
        ses.save()
    else:
        return redirect("/cart/" + str(post_id) + "/remove/")

    return redirect("/cart/")


################
@login_required(login_url='/login/accounts/login')
def Item_Delete(request, post_id):
    ses = session.objects.get(id=post_id)
    if not ses.name.title == "donate":
        a = BlogStats.objects.get(blog=ses.name, user=request.user)
        a.rating = 0
        a.save()
    ses.delete()
    return redirect("/cart/")


################
@login_required(login_url='/login/accounts/login')
def Checkout(request):
    ses = session.objects.filter(user=request.user)
    total = 0
    for s in ses:
        total += s.price()
    # generate all other required data that you may need on the #checkout page and add them to context.
    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox
    # Configure Braintree
    braintree.Configuration.configure(
        braintree_env,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )
    try:
        braintree_client_token = braintree.ClientToken.generate({"customer_id": user.id})
    except:
        braintree_client_token = braintree.ClientToken.generate({})
    template_name = "cart/checkout.html"
    context = {"sessions": ses, "total": total, 'braintree_client_token': braintree_client_token}
    return render(request, template_name, context)


# 333333333############  pAYMENT ######################
@login_required(login_url='/login/accounts/login')
def payment(request):
    nonce_from_the_client = request.POST['paymentMethodNonce']
    ses = session.objects.filter(user=request.user)
    total = 0
    for s in ses:
        total += s.price()
    customer_kwargs = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": str(total),
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    print(result)
    return redirect("/cart/complete/")


@login_required(login_url='/login/accounts/login')
def Complete(request):
    ses = session.objects.filter(user=request.user)
    for s in ses:
        if not s.name.title == 'donate':
            s.name.votes += s.votes
            s.name.value += s.votes * 10
            s.name.save()
            a = BlogStats.objects.get(blog=s.name, user=request.user)
            a.rating = 0
            a.save()
        s.delete()
    return redirect("/")


class CheckoutView(generic.FormView):
    """This view lets the user initiate a payment."""
    form_class = forms.CheckoutForm
    template_name = 'cart/checkout.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # We need the user to assign the transaction
        self.user = request.user

        # Ha! There it is. This allows you to switch the
        # Braintree environments by changing one setting
        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        # Configure Braintree
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )
        # Generate a client token. We'll send this to the form to
        # finally generate the payment nonce
        # You're able to add something like ``{"customer_id": 'foo'}``,
        # if you've already saved the ID
        self.braintree_client_token = braintree.ClientToken.generate({})
        return super(CheckoutView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
            ctx = super(CheckoutView, self).get_context_data(**kwargs)
            ctx.update({
                'braintree_client_token': self.braintree_client_token,
            })
            return ctx


    def form_valid(self, form):
            # Braintree customer info
            # You can, for sure, use several approaches to gather customer infos
            # For now, we'll simply use the given data of the user instance
            customer_kwargs = {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            }

            # Create a new Braintree customer
            # In this example we always create new Braintree users
            # You can store and re-use Braintree's customer IDs, if you want to
            result = braintree.Customer.create(customer_kwargs)
            if not result.is_success:
                # Ouch, something went wrong here
                # I recommend to send an error report to all admins
                # , including ``result.message`` and ``self.user.email``

                context = self.get_context_data()
                # We re-generate the form and display the relevant braintree error
                context.update({
                    'form': self.get_form(self.get_form_class()),
                    'braintree_error': u'{} {}'.format(
                        result.message, _('Please get in contact.'))
                })
                return self.render_to_response(context)

            # If the customer creation was successful you might want to also
            # add the customer id to your user profile
            customer_id = result.customer.id

            """
            Create a new transaction and submit it.
            I don't gather the whole address in this example, but I can
            highly recommend to do that. It will help you to avoid any
            fraud issues, since some providers require matching addresses

            """
            address_dict = {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "street_address": 'street',
                "extended_address": 'street_2',
                "locality": 'city',
                "region": 'state_or_region',
                "postal_code": 'postal_code',
                "country_code_alpha2": 'alpha2_country_code',
                "country_code_alpha3": 'alpha3_country_code',
                "country_name": 'country',
                "country_code_numeric": 'numeric_country_code',
            }

            # You can use the form to calculate a total or add a static total amount
            # I'll use a static amount in this example
            result = braintree.Transaction.sale({
                "customer_id": customer_id,
                "amount": total,
                "payment_method_nonce": form.cleaned_data['payment_method_nonce'],
                "descriptor": {
                    # Definitely check out https://developers.braintreepayments.com/reference/general/validation-errors/all/python#descriptor
                    "name": "COMPANY.*test",
                },
                "billing": address_dict,
                "shipping": address_dict,
                "options": {
                    # Use this option to store the customer data, if successful
                    'store_in_vault_on_success': True,
                    # Use this option to directly settle the transaction
                    # If you want to settle the transaction later, use ``False`` and later on
                    # ``braintree.Transaction.submit_for_settlement("the_transaction_id")``
                    'submit_for_settlement': True,
                },
            })
            if not result.is_success:
                # Card could've been declined or whatever
                # I recommend to send an error report to all admins
                # , including ``result.message`` and ``self.user.email``
                context = self.get_context_data()
                context.update({
                    'form': self.get_form(self.get_form_class()),
                    'braintree_error': _(
                        'Your payment could not be processed. Please check your'
                        ' input or use another payment method and try again.')
                })
                return self.render_to_response(context)

            # Finally there's the transaction ID
            # You definitely want to send it to your database
            transaction_id = result.transaction.id
            # Now you can send out confirmation emails or update your metrics
            # or do whatever makes you and your customers happy :)
            return super(CheckoutView, self).form_valid(form)

    def get_success_url(self):
            # Add your preferred success url
            return redirect('/cart/complete/')



