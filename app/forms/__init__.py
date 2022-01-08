'''
form/__init__.py
'''

from app.forms.add_address import AddAddressForm
from app.forms.add_to_cart import AddToCartForm
from app.forms.checkout import CheckoutForm
from app.forms.forgot_password import ForgotPasswordForm
from app.forms.login import LoginForm
from app.forms.new_category import NewCategoryForm
from app.forms.new_discount import (
    NewShippingDiscountForm, NewProductDiscountForm, NewOrderDiscountForm
)
from app.forms.new_product import NewProductForm
from app.forms.new_user import (
    NewStaffForm, NewCustomerForm
)
from app.forms.redeem_code import RedeemCodeForm
from app.forms.register import RegisterForm
from app.forms.reset_password import ResetPasswordForm
from app.forms.search import SearchForm
from app.forms.update_profile import UpdateProfileForm
