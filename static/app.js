const labels = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
];
const data = {
  labels: labels,
  datasets: [{
    label: 'My First dataset',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 2, 20, 30, 45],
  }]
};

const config = {
  type: 'line',
  data,
  options: {}
};

const myChart = new Chart(
  document.getElementById('myChart'),
  config
);

const populateDataSource= function(data) {
  $('#dataSource').val(JSON.stringify(data, undefined, 2));
  M.textareaAutoResize($('#dataSource'));
}

$(document).ready(function(){
  M.updateTextFields();
  $('.collapsible').collapsible();
  $('select').formSelect();

  const defaultData = {data:[]}
  populateDataSource(defaultData)

  $('#geoTypeSelector').on('change', function() {
    $.get('/api/regions?geoType=' + $(this).val(), function(data, status){
      if (status === 'success') {
        $el = $('#regionSelector')
        $el.empty();
        $el.append($('<option></option>').attr('disabled', true).text('Choose one'));
        $el.append($('<option value="all">Select All</option>').attr('selected', true));
        data.regions.forEach((region) => {
          $el.append($('<option></option>').attr('value', region.id).text(region.name));
        })
        $('select').formSelect();
      } else {
        console.error(status)
      }
    });
  })

  $('#filter-form').on('submit', function(e) {
    e.preventDefault();
    $.ajax({
        url: '/api/traffic',
        data: $('#filter-form').serialize(),
        type: 'POST',
        success: function(response) {
          populateDataSource(response.locations)
        },
        error: function(error) {
          console.error(error);
        }
    });
  });

  $('#publish-form').on('submit', function(e) {
    e.preventDefault();
  })
});