/* jshint esversion: 6 */




// index image carousel

const track = document.querySelector('.carousel__track');

if (track) {
    const track = document.querySelector('.carousel__track');
    const slides = Array.from(track.children);
    const slideWidth = slides[0].getBoundingClientRect().width;

// Arrange the slides next to one another
    const setSlidePosition = (slide, index) => {
         slide.style.left = slideWidth * index + 'px';
    };
    slides.forEach(setSlidePosition);

// Move to next slide every 3 seconds
    setInterval(() => {
        const currentSlide = track.querySelector('.current-slide');
        const nextSlide = currentSlide.nextElementSibling || slides[0];
    
    // Move to the next slide
        track.style.transform = 'translateX(-' + nextSlide.style.left + ')';
        currentSlide.classList.remove('current-slide');
        nextSlide.classList.add('current-slide');
    }, 3000);
}

// Stripe Js payment form 
// To use this payment method live, you must switch to HTTPs to ensure secure data transfer

var stripe = Stripe('pk_test_51Own3jFlpTEzDIrEWgl8A3ChU9v5tddxPbVh8VTxHJJHAXU0nzAVBRGGvap56gncNJuVudSf0uixGMrU77It6sUV00qCFkadDE');
var elements = stripe.elements();

var card = elements.create('card');

// Check if #card-element exists before mounting
if (document.querySelector('#card-element')) {
    card.mount('#card-element');
}

var form = document.getElementById('payment-form');
if (form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        stripe.createToken(card).then(function(result) {
            if (result.error) {
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
                stripeTokenHandler(result.token);
            }
        });
    });
}

// Submit Stripe form to Django

function stripeTokenHandler(token) {
    var form = document.getElementById('payment-form');
    if (form) {
        var hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', token.id);
        form.appendChild(hiddenInput);

        form.submit();
    }
}

// Validate review rating field max value 10 REVIEWS PAGE FORM

window.onload = function() {
    var reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(event) {
            var rating = document.getElementById('rating').value;
            if (rating < 1 || rating > 10) {
                alert('Rating must be between 1 and 10.');
                event.preventDefault();
            }
        });
    }
};




console.log("JavaScript is being loaded!");