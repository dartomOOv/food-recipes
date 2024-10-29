document.addEventListener("DOMContentLoaded", function () {
  document.querySelector('.btn.btn-success').addEventListener('click', function () {
    let newRow = document.querySelector('#empty-form-row table').innerHTML;
    document.querySelector('#ingredients-table tbody').insertAdjacentHTML('beforeend', newRow);
  });

  document.querySelector('#ingredients-table').addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-danger')) {
      e.target.closest('tr').remove();
    }
  });
});