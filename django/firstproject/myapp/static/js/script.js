document.addEventListener('DOMContentLoaded', function() {
  const button = document.getElementById('myButton');
  if (button) {
    button.addEventListener('click', function() {
      alert('Button clicked');
    });
  }
});
