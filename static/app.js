const CHART_COLORS = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)'
}

const NAMED_COLORS = [
  CHART_COLORS.red,
  CHART_COLORS.orange,
  CHART_COLORS.yellow,
  CHART_COLORS.green,
  CHART_COLORS.blue,
  CHART_COLORS.purple,
  CHART_COLORS.grey,
]

const namedColor = function(index) {
  return NAMED_COLORS[index % NAMED_COLORS.length];
}

const labels = [];
const data = {
  labels: labels,
  datasets: [{
    label: '',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [],
  }]
}

const config = {
  type: 'line',
  data,
  options: {
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  }
}

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
  $('.collapsible').collapsible({
    accordion: false
  });
  $('select').formSelect();

  const defaultData = []
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