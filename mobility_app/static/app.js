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

$(document).ready(function(){
  M.updateTextFields();
  $('.collapsible').collapsible();
  $('select').formSelect();

  const defaultData = {data:[]}
  $('#json_source').val(JSON.stringify(defaultData, undefined, 2));
  M.textareaAutoResize($('#json_source'));

  $('#geoTypeSelector').on('change', function(e) {
    $.get('/api/regions?geoType=' + $(this).val(), function(data, status){
      if (status === 'success') {
        console.log(data)
        $el = $('#regionSelector')
        $el.empty().append($("<option></option>").attr('disabled', true).attr('selected', true).text('Choose one'));
        data.regions.forEach((region) => {
          $el.append($("<option></option>").attr("value", region.id).text(region.name));
        })
        $('select').formSelect();
      }
    });
  })
});