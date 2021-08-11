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
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      }
    },
    scales: {
      x: {
        grid: {
          display: true,
          drawBorder: true,
          drawOnChartArea: true,
          drawTicks: true,
        }
      },
      y: {
        grid: {
          drawBorder: false,
          color: function(context) {
            if (context.tick.value == 100) {
              return '#000000'
            }
            return '#cccccc'
          },
        },
      }
    }
  }
}

let currentRegions = []
let datasetList = []
let selectedDataset = []

const dataChart = new Chart(
  document.getElementById('dataChart'),
  config
)

const buildRegionLabel = function(region) {
  let regionLabel = ''
  if (region.region_name) {
    regionLabel = `${region.region_name}`

    if (region.sub_region) {
      regionLabel = `${region.region_name}, ${region.sub_region}`
    }
  } else {
    regionLabel = `${region.region}`

    if (region['sub-region']) {
      regionLabel = `${region.region}, ${region['sub-region']}`
    }
  }

  if (region.country) {
    regionLabel = `${regionLabel}, ${region.country}`
  }

  return regionLabel
}

const buildDatasetLabel = function(row, dataType) {
  let datasetLabel = `${row.region_name}`

  if (row.sub_region) {
    datasetLabel = `${row.region_name}, ${row.sub_region}`
  }

  if (row.country) {
    datasetLabel = `${datasetLabel}, ${row.country}`
  }

  return `${dataType} (${datasetLabel})`
}

const buildDataSet = function(row, data, label) {
  dataChart.data.datasets.push(
    {
      label: buildDatasetLabel(row, label),
      borderColor: namedColor(dataChart.data.datasets.length),
      data: Object.entries(data).map(([key, value]) => {
        return {x: key, y: value}
      }),
    }
  )
  dataChart.update()
}

const resetData = function(chart) {
  $('#currentDatasetLabel').empty()
  while(chart.data.datasets.length > 0) {
    chart.data.datasets.pop();
  }
  chart.update()
}

const toggleDataset = function(index) {
  let indexPos = selectedDataset.indexOf(index)

  if (indexPos < 0) {
    selectedDataset.push(index)
  } else {
    delete selectedDataset[indexPos]
  }

  selectedDataset = selectedDataset.flat()

  resetData(dataChart)

  selectedDataset.forEach( idx => {
    let region = datasetList[idx]
    setCurrentDataset(region)
  })

  const selectedRegions = selectedDataset.map( idx => {
    return datasetList[idx]
  })

  $('#dataSource').val(JSON.stringify(selectedRegions, undefined, 2))
  M.textareaAutoResize($('#dataSource'))
}

const setCurrentDataset = function(region) {
  // $('#currentDatasetLabel').text(`(${buildRegionLabel(region)})`)

  if (region.direction_requests.transit && Object.values(region.direction_requests.transit).length > 0) {
    buildDataSet(region, region.direction_requests.transit, 'Transit')
  }

  if (region.direction_requests.driving && Object.values(region.direction_requests.driving).length > 0) {
    buildDataSet(region, region.direction_requests.driving, 'Driving')
  }

  if (region.direction_requests.walking && Object.values(region.direction_requests.walking).length > 0) {
    buildDataSet(region, region.direction_requests.walking, 'Walking')
  }
}

const populateDatasetList = function() {
  $el = $('#dataset-list')
  $el.empty()

  for (let i = 0; i < datasetList.length; i++) {
    const region = datasetList[i]

    let $input = $(`<input type="checkbox" class="filled-in dataset-selector" name="selectedDataset${i}" id="selectedDataset${i}" value="${i}" />`)
    $input.on('click', function(e) {
      let idx = parseInt($(e.target).val())
      console.log('Toggling Dataset', idx)
      toggleDataset(idx)
    })
    let $datasetSelector = $('<label></label>').append($input)
    $('<span></span>').insertAfter($input)

    let $cell = $('<p></p>').append($datasetSelector)
    let $action = $('<td></td>').append($cell)

    let row = $(`<tr><td>${region.geo_type}</td><td>${buildRegionLabel(region)}</td></tr>`)
    row.append($action)

    $el.append(row)
  }
}

const populateDataSource = function(data, transportTypeToDisplay = { transit: true, walking: true, driving: true }) {
  data.forEach( row => {
    if (!transportTypeToDisplay.transit) {
      delete row.direction_requests['transit']
    }

    if (!transportTypeToDisplay.driving) {
      delete row.direction_requests['driving']
    }

    if (!transportTypeToDisplay.walking) {
      delete row.direction_requests['walking']
    }
  })

  datasetList = data

  populateDatasetList()
  resetData(dataChart)
  selectedDataset = []

  if (datasetList.length > 0) {
    toggleDataset(0)
    $('#selectedDataset0').attr('checked', 'checked')
  }
}

const isFormFieldChecked = function(form, fieldName) {
  return form.serializeArray().filter( field => field.name == fieldName).length > 0
}

const transportTypeToDisplay = function(form) {
  return {
    transit: isFormFieldChecked(form, 'showTransit'),
    walking: isFormFieldChecked(form, 'showWalking'),
    driving: isFormFieldChecked(form, 'showDriving'),
  }
}

const validateData = function(regions) {
  let shouldPrompt = false

  let maxAllowable = parseInt($('#maxTrafficRequestAllowed').val())
  if ( isNaN(maxAllowable)) {
    maxAllowable = 3000
  }

  regions.forEach( regionData => {
    ['transit', 'driving', 'walking'].forEach( trafficType => {
      if (regionData.direction_requests[trafficType]) {
        Object.values(regionData.direction_requests[trafficType]).forEach( dataPoint => {
          if (dataPoint > maxAllowable) {
            shouldPrompt = true
          }
        })
      }
    })
  })

  if (shouldPrompt) {
    return confirm(`There are traffic values that are higher than the maximum allowable limit of ${maxAllowable}.\n\nDo you want to allow this?`)
  }

  return true
}

const lockDataset = function(regionData) {
  try {
    const transportationType = []

    const transportationTypes = ['transit', 'driving', 'walking']
    transportationTypes.forEach( trafficType => {
      if (regionData.direction_requests[trafficType]) {
        transportationType.push(trafficType)
      }
    })

    if (transportationType.length < 1) {
      return
    }

    const formData = {
      region: regionData.region_name,
      sub_region: regionData.sub_region,
      transportation_type: transportationType.join(','),
      lock: true
    }

    $.ajax({
      url: '/api/traffic/lock',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(formData),
      success: function(response) {
        console.log('Locked Data for:', transportationType.join(','))
      },
      error: function(error) {
        console.error(error)
        alert(error.message)
      }
    })
  }
  catch(err) {
    console.error(err)
    alert(err.message)
  }
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
    $.get('/api/regions/' + $(this).val(), function(data, status){
      if (status === 'success') {
        $el = $('#regionSelector')
        $el.empty();
        $el.append($('<option></option>').attr('disabled', true).attr('selected', true).text('Choose one'));

        currentRegions = data.regions

        for (let i = 0; i < currentRegions.length; i++) {
          const region = currentRegions[i]
          $el.append($('<option></option>').attr('value', i).text(buildRegionLabel(region)))
        }

        $('select').formSelect();
      } else {
        console.error(status)
      }
    });
  })

  $('#filter-region-form').on('submit', function(e) {
    e.preventDefault();

    try {
      if ( $('#regionSelector').val() == null || $('#regionSelector').val().length === 0 ) {
        throw Error('Please select a region.')
      }

      const regionIndex = parseInt($('#regionSelector').val())
      const region = currentRegions[regionIndex]

      let searchParams = {
        region: region.region,
        sub_region: region['sub-region']
      }
      searchParams = Object.assign(searchParams, transportTypeToDisplay($('#filter-region-form')))

      $.ajax({
        url: '/api/traffic',
        data: searchParams,
        type: 'GET',
        success: function(response) {
          populateDataSource(response.regions, transportTypeToDisplay($('#filter-region-form')))
        },
        error: function(error) {
          console.error(error)
          alert(error.message)
        }
      });
    }
    catch(err) {
      alert(err.message)
    }
  })

  $('#filter-traffic-form').on('submit', function(e) {
    e.preventDefault();
    $('#filter-traffic-form-loader').removeClass('hide')

    let searchParams = {
      traffic_filter_type: $('#trafficFilterType').val(),
      traffic_filter_amount: $('#trafficFilterAmt').val()
    }
    searchParams = Object.assign(searchParams, transportTypeToDisplay($('#filter-traffic-form')))

    try {
      $.ajax({
        url: '/api/traffic/filter',
        data: searchParams,
        type: 'GET',
        success: function(response) {
          populateDataSource(response.regions, transportTypeToDisplay($('#filter-traffic-form')))
          $('#filter-traffic-form-loader').addClass('hide')
        },
        error: function(error) {
          console.error(error)
          alert(error.message)
        }
    });
    }
    catch(err) {
      $('#filter-traffic-form-loader').addClass('hide')
      alert(err.message)
    }
  })


  $('#updateChart').on('click', function(e) {
    e.preventDefault();

    try {
      const jsonData = JSON.parse($('#dataSource').val())

      for (let i = 0; i < selectedDataset.length; i++) {
        const key = selectedDataset[i]
        datasetList[key] = jsonData[i]
      }

      orgSelectedDataset = [...selectedDataset]
      selectedDataset = []

      orgSelectedDataset.forEach( idx => {
        toggleDataset(idx)
      })
    }
    catch(err) {
      console.error(err)
      alert(err.message)
    }
  })

  $('#publish-form').on('submit', function(e) {
    e.preventDefault();

    try {
      const jsonData = JSON.parse($('#dataSource').val())

      if (validateData(jsonData)) {
        jsonData.forEach( regionData => {
          let formData = {
            region: regionData.region_name,
            sub_region: regionData.sub_region,
            traffic: regionData.direction_requests
          }

          $.ajax({
            url: '/api/traffic',
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
              if (response.hasOwnProperty('error')) {
                console.error('Error:', response.error)
                alert(`Error: ${response.error}`)
              } else {
                if (isFormFieldChecked($('#publish-form'), 'lockData')) {
                  lockDataset(regionData)
                  alert(`New data for ${regionData.region_name} has been published and locked.`)
                } else {
                  alert(`New data for ${regionData.region_name} has been published.`)
                }
              }
            },
            error: function(error) {
              console.error(error)
              alert(error.message)
            }
          })
        })
      }
    }
    catch(err) {
      alert(err.message)
    }
  })
});