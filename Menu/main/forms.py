
from django import forms
from django.core.validators import RegexValidator
from .models import Cart, CartItem, Customer, Contact, Reservation, CateringRequest, GiftCardRequest
import re

class CartItemUpdateForm(forms.Form):
    """Form for updating cart item quantity"""
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, 
        max_value=50, 
        initial=1,
        error_messages={
            'required': 'Please enter a quantity.',
            'min_value': 'Quantity must be at least 1.',
            'max_value': 'Maximum quantity allowed is 50.',
            'invalid': 'Please enter a valid number.'
        }
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control text-center',
            'style': 'width: 80px; display: inline-block;',
            'data-validation': 'quantity'
        })

class CartItemRemoveForm(forms.Form):
    """Form for removing cart item"""
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())

class AddToCartForm(forms.Form):
    """Form for adding items to cart"""
    item_type = forms.ChoiceField(
        choices=[('food', 'Food'), ('special', 'Special')],
        error_messages={
            'required': 'Please select an item type.',
            'invalid_choice': 'Please select a valid item type.'
        }
    )
    item_id = forms.IntegerField(
        error_messages={
            'required': 'Item ID is required.',
            'invalid': 'Please select a valid item.'
        }
    )
    quantity = forms.IntegerField(
        min_value=1, 
        max_value=50, 
        initial=1,
        error_messages={
            'required': 'Please enter a quantity.',
            'min_value': 'Quantity must be at least 1.',
            'max_value': 'Maximum quantity allowed is 50.',
            'invalid': 'Please enter a valid number.'
        }
    )

class CheckoutForm(forms.ModelForm):
    """Form for checkout process with support for delivery and dine-in orders"""
    
    ORDER_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('dine_in', 'Dine In'),
    ]
    
    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'order-type-radio'}),
        initial='delivery',
        error_messages={
            'required': 'Please select an order type.',
            'invalid_choice': 'Please select a valid order type.'
        }
    )
    
    # Phone number validator
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be 9-15 digits. Format: '+999999999' or '999999999'"
    )
    
    table_number = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Table Number (e.g., T-01, A5)',
            'data-validation': 'table-number'
        }),
        error_messages={
            'max_length': 'Table number cannot exceed 10 characters.'
        }
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('cash', 'Cash Payment'),
            ('card', 'Card Payment'),
            ('wallet', 'Digital Wallet')
        ],
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'}),
        error_messages={
            'required': 'Please select a payment method.',
            'invalid_choice': 'Please select a valid payment method.'
        }
    )
    
    order_notes = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Special instructions (optional)',
            'class': 'form-control',
            'data-validation': 'notes'
        }),
        error_messages={
            'max_length': 'Order notes cannot exceed 500 characters.'
        }
    )
    
    class Meta:
        model = Customer
        fields = ['customer_firstname', 'customer_lastname', 'customer_mobileno', 'customer_address', 'customer_email']
        widgets = {
            'customer_firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True,
                'data-validation': 'first-name'
            }),
            'customer_lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True,
                'data-validation': 'last-name'
            }),
            'customer_mobileno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True,
                'data-validation': 'phone'
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Delivery Address',
                'required': False,
                'data-validation': 'address'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True,
                'data-validation': 'email'
            }),
        }
        error_messages = {
            'customer_firstname': {
                'required': 'First name is required.',
                'max_length': 'First name cannot exceed 100 characters.'
            },
            'customer_lastname': {
                'required': 'Last name is required.',
                'max_length': 'Last name cannot exceed 100 characters.'
            },
            'customer_mobileno': {
                'required': 'Phone number is required.',
                'invalid': 'Please enter a valid phone number.'
            },
            'customer_address': {
                'max_length': 'Address cannot exceed 500 characters.'
            },
            'customer_email': {
                'required': 'Email address is required.',
                'invalid': 'Please enter a valid email address.'
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make address not required by default - we'll handle this with JavaScript
        self.fields['customer_address'].required = False
        
        # Add phone validator to mobile field
        self.fields['customer_mobileno'].validators = [self.phone_validator]
        
        # Enhanced validation attributes for better UX
        for field_name, field in self.fields.items():
            if field_name in self.Meta.fields:
                field.widget.attrs['data-field'] = field_name
    
    def clean_customer_firstname(self):
        firstname = self.cleaned_data.get('customer_firstname')
        if firstname:
            if len(firstname.strip()) < 2:
                raise forms.ValidationError('First name must be at least 2 characters long.')
            if not re.match(r'^[a-zA-Z\s]+$', firstname):
                raise forms.ValidationError('First name can only contain letters and spaces.')
        return firstname
    
    def clean_customer_lastname(self):
        lastname = self.cleaned_data.get('customer_lastname')
        if lastname:
            if len(lastname.strip()) < 2:
                raise forms.ValidationError('Last name must be at least 2 characters long.')
            if not re.match(r'^[a-zA-Z\s]+$', lastname):
                raise forms.ValidationError('Last name can only contain letters and spaces.')
        return lastname
    
    def clean_customer_email(self):
        email = self.cleaned_data.get('customer_email')
        if email:
            # Additional email validation
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        customer_address = cleaned_data.get('customer_address')
        table_number = cleaned_data.get('table_number')
        
        if order_type == 'delivery':
            if not customer_address or not customer_address.strip():
                raise forms.ValidationError('Delivery address is required for delivery orders.')
            elif len(customer_address.strip()) < 10:
                raise forms.ValidationError('Please provide a more detailed delivery address (at least 10 characters).')
        elif order_type == 'dine_in':
            if not table_number or not table_number.strip():
                raise forms.ValidationError('Table number is required for dine-in orders.')
            elif not re.match(r'^[A-Za-z0-9\-]{1,10}$', table_number.strip()):
                raise forms.ValidationError('Table number format is invalid. Use letters, numbers, and hyphens only.')
        
        return cleaned_data

class ContactForm(forms.ModelForm):
    """Form for contact submissions"""
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Your Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Your Phone Number',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Your Message / Feedback',
                'rows': 10,
                'cols': 30,
                'required': True
            })
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'min': 1, 'max': 20, 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Any special requests?'}),
        }

class CateringRequestForm(forms.ModelForm):
    class Meta:
        model = CateringRequest
        fields = ['name', 'email', 'phone', 'event_date', 'event_type', 'guests', 'message']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'min': 1, 'max': 500, 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe your event or requests'}),
        }

class GiftCardRequestForm(forms.ModelForm):
    class Meta:
        model = GiftCardRequest
        fields = ['name', 'email', 'phone', 'amount', 'recipient_name', 'recipient_email', 'message']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': 100, 'max': 10000, 'step': 100, 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Personal message for recipient'}),
        }
