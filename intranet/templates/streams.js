function get_channels() {
  $.ajax({
    type : "GET",
    url : "{% url 'get_channels' %}",
    data : {},
    dataType : "json",
    success : list_channels,
  });
  //$.ajax({
  //  type : "GET",
  //  url : "{% url 'get_videos' %}",
  //  data : {},
  //  dataType : "json",
  //  success : list_videos,
  //});
};

function get_streams() {
  $.ajax({
    type : "GET",
    url : "{% url 'update_streams' %}",
    processData : true,
    data : {},
    dataType : "json",
    success : update_list,
    cache : true,
  });
};

function create_container() {
  var container = $(' <tr class="channel"><td class="channel-logo"><img class="img-rounded" /></td> <td><a class="channel-title"><strong></strong></a> <span class="channel-game"></span><br /> <small class="channel-status"></small> </td></tr> ');
  return container;
};

function list_channels(data) {
  $.each(data, function(index, channel) {
    container = create_container();
    update_stream(container, channel);
  });
};

function update_stream(container, channel) {
  container.attr('stream', channel.name);
  container.find('td.channel-logo img').attr('src', channel.logo);
  container.find('a.channel-title strong').text(channel.display_name);
  container.find('a.channel-title').attr('href', channel.url).attr('alt', channel.name);
  if (channel.game != null) {
    container.find('span.channel-game').text(' playing ' + channel.game);
  } else {
    container.find('span.channel-game').text('');
  };
  container.find('small.channel-status').text(channel.status);
  if (channel.streaming && ! container.hasClass('success')) {
    container.removeClass('info').addClass('success');
    $('tr#stream-separator').before(container);
  } else if (!channel.streaming && ! container.hasClass('info')) {
    container.removeClass('success').addClass('info');
    $('tbody#channels').append(container);
  };
};

function list_videos(data) {
};

function update_list(data) {
  $.each(data, function(index, stream) {
    var container = $('tr[stream=' + stream.name + ']');
    if (container.length == 0) {
      container = create_container();
    };
    update_stream(container, stream);
  });
};

$(document).ready(function() {
  get_channels();
  var update_streams = function() {
    get_streams();
    setTimeout(update_streams, 30000);
  };
  update_streams();
});

$(function() {
  $("#submit_add").click(function() {
    $.ajax({
      type : "GET",
      url : "{% url 'add_stream' %}",
      data : {'channel' : $("input#add_stream").val()},
      dataType : "json",
      success : confirm_add,
    });
    return false;
  });
});

function confirm_add(data) {
  update_streams();
};

$(function() {
  $("#stream-separator").click(function() {
    $("tr.channel.info").toggle();
  });
});
