from django import forms
from .models import Cart, CartItem, Customer, Contact, Reservation, CateringRequest, GiftCardRequest

class CartItemUpdateForm(forms.Form):
    """Form for updating cart item quantity"""
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, max_value=50, initial=1)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control text-center',
            'style': 'width: 80px; display: inline-block;'
        })

class CartItemRemoveForm(forms.Form):
    """Form for removing cart item"""
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())

class AddToCartForm(forms.Form):
    """Form for adding items to cart"""
    item_type = forms.ChoiceField(choices=[('food', 'Food'), ('special', 'Special')])
    item_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=1, max_value=50, initial=1)

class CheckoutForm(forms.ModelForm):
    """Form for checkout process with support for delivery and dine-in orders"""
    
    ORDER_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('dine_in', 'Dine In'),
    ]
    
    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'order-type-radio'}),
        initial='delivery'
    )
    
    table_number = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Table Number (e.g., T-01, A5)'
        })
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('cash', 'Cash Payment'),
            ('card', 'Card Payment'),
            ('wallet', 'Digital Wallet')
        ],
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'})
    )
    
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Special instructions (optional)',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Customer
        fields = ['customer_firstname', 'customer_lastname', 'customer_mobileno', 'customer_address', 'customer_email']
        widgets = {
            'customer_firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'customer_lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'customer_mobileno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Delivery Address',
                'required': False  # Will be required conditionally
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make address not required by default - we'll handle this with JavaScript
        self.fields['customer_address'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        customer_address = cleaned_data.get('customer_address')
        table_number = cleaned_data.get('table_number')
        
        if order_type == 'delivery':
            if not customer_address:
                raise forms.ValidationError('Delivery address is required for delivery orders.')
        elif order_type == 'dine_in':
            if not table_number:
                raise forms.ValidationError('Table number is required for dine-in orders.')
        
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
