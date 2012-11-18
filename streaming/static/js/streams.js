function get_channels(channels) {
  $.each(channels, function(index, channel) {
    $.ajax({
      type : "GET",
      url : "https://api.twitch.tv/kraken/channels/" + channel,
      data : {},
      dataType : "jsonp",
      success : describe_channel,
    });
    $.ajax({
      type : "GET",
      url : "https://api.twitch.tv/kraken/channels/" + channel + '/videos?limit=3',
      data : {},
      dataType : "jsonp",
      success : list_videos(channel),
    });
  });
};

function list_videos(user) {
  return function list_videos(data) {
    $.each(data.videos, function(index, video) {
      var element = $('<li><a href="' + video.url + '">' + video.title +
        ' (' + video.recorded_at + ')</a></li>');
      $("div[channel=" + user + "] ul").append(element);
    });
  };
};

function describe_channel(data) {
  $("div[channel=" + data.name + "] img.stream-logo").attr("src", data.logo);
  $("div[channel=" + data.name + "] h6.stream-name a").html(data.display_name);
  $("div[channel=" + data.name + "] p.stream-status").html(
      data.status + "(" + data.game + ")");
};

function get_streams() {
  var channels = $("div[channel]").map(function() { return $(this).attr("channel");});
  $.ajax({
    type : "GET",
    url : "https://api.twitch.tv/kraken/streams?channel=" + channels.get(),
    processData : true,
    data : {},
    dataType : "jsonp",
    success : render_list,
    cache : true,
  });
};

function render_list(data) {
  var good = Array();
  $.each(data.streams, function(index, stream) {
    var name = stream.channel.name;
    good.push(name);
    describe_channel(stream.channel);
    $("div[channel=" + name + "]").removeClass("text-info").addClass("text-error");

  });
  $("div[channel]").each(function() {
    if ($.inArray($(this).attr("channel"), good) == -1) {
      $(this).removeClass("text-error").addClass("text-info");
    };
  });
};

$(document).ready(function() {
  var channels = $("div[channel]").map(function() { return $(this).attr("channel");});
  get_channels(channels);
  var update_streams = function() {
    get_streams();
    setTimeout(update_streams, 30000);
  };
  update_streams(channels);
});
