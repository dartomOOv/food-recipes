document.querySelector('.btn.btn-success').addEventListener('click', function() {
  let newRow = `
    <tr>
      <td>
        <select name="ingredients[]" class="ingredient-select">
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="carrot">Carrot</option>
        </select>
      </td>
      <td>
        <input type="text" name="amounts[]" class="ingredient-amount" placeholder="e.g., 2 pieces/2 liters"/>
      </td>
      <td>
        <button type="button" class="btn btn-danger">Remove</button>
      </td>
    </tr>
  `;
  document.querySelector('#ingredients-table tbody').insertAdjacentHTML('beforeend', newRow);
});

document.querySelector('#ingredients-table').addEventListener('click', function(e) {
  if (e.target.classList.contains('btn-danger')) {
    e.target.closest('tr').remove();
  }
});
