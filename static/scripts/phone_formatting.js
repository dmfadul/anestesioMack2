document.addEventListener('DOMContentLoaded', (event) => {
  const phoneInput = document.getElementById('phoneNum');

  phoneInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 2 && value.length <= 7)
      value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
    else if (value.length > 7)
      value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7)}`;
    e.target.value = value;
  });
});
