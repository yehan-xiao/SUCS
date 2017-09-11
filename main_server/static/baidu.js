//Written by Shitao Tang
map = new BMap.Map("container");
var get_rect;
var get_point;
function change_mode(button) {
    jQuery("#rect").css("background-color", "#009FE3");
    jQuery("#point").css("background-color", "#009FE3");
    jQuery("#normal").css("background-color", "#009FE3");
    button.css("background-color", "#ccc");
}


function remove_all_listener() {
    map.removeEventListener("click", get_rect);
    map.removeEventListener("click", get_point);
}
marker1 = null;
marker2 = null;
polygon = null;
function normal() {
    change_mode(jQuery("#normal"));
    remove_all_listener();
    map.removeOverlay(marker1);
    map.removeOverlay(marker2);
    min_lng = null, min_lat = null, max_lng = null, max_lat = null;
}

function draw_rect() {
    change_mode(jQuery("#rect"));
    remove_all_listener();
    get_rect = function (e) {
        var pt = new BMap.Point(e.point.lng, e.point.lat);
        var myIcon = new BMap.Icon("/static/img/dot.png", new BMap.Size(30, 30));
        if (min_lng == null) {
            marker1 = new BMap.Marker(pt, { icon: myIcon });
            map.addOverlay(marker1);
            min_lat = e.point.lat;
            min_lng = e.point.lng;
        }
        else {
            marker2 = new BMap.Marker(pt, { icon: myIcon });
            map.addOverlay(marker2);
            max_lat = e.point.lat;
            max_lng = e.point.lng;
            if (min_lat > max_lat) {
                [min_lat, max_lat] = [max_lat, min_lat];
            }
            if (min_lng > max_lng) {
                [min_lng, max_lng] = [max_lng, min_lng];
            }

            polygon = new BMap.Polygon([
                new BMap.Point(min_lng, min_lat),
                new BMap.Point(min_lng, max_lat),
                new BMap.Point(max_lng, max_lat),
                new BMap.Point(max_lng, min_lat)
            ], { strokeColor: "lightblue", strokeWeight: 6, strokeOpacity: 0.5 });
            map.addOverlay(polygon);
            $('#searching_window, #overlay-back').fadeIn(500);
            $('#search_by_name').on('click', { min_lng, min_lat, max_lng, max_lat }, search_by_name);
        }
    }
    map.addEventListener("click", get_rect);
}

function search_coordinate() {
    change_mode(jQuery("#point"));
    get_point = function (e) {
        var lat = e.point.lat, lng = e.point.lng;
        var url = "http://api.map.baidu.com/panorama/v2?ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb&width=1000&height=512&location=" + lng + "," + lat + "&fov=120&pitch=40&heading=90";
        var image = { "bounding_box": [], "lat": lat, "long": lng, "url": url };
        add_marker(image);
        map.removeEventListener("click", get_point);
        normal();
    }
    map.addEventListener("click", get_point);
}

function close_searching_window() {
    map.removeOverlay(marker1);
    map.removeOverlay(marker2);
    map.removeOverlay(polygon);
    $("#image_analysis").attr("disabled", true);
    $('#searching_window, #overlay-back').fadeOut(500);
    normal();
}

function close_image_window() {
    $('#image_window, #overlay-back').fadeOut(500);
    normal();
}

function search_by_name() {
    var placename = jQuery("#placename").val();
    if (placename == "") {
        alert("Place name must be specified");
        return;
    }
    $('body').addClass("loading");
    jQuery.ajax({
        type: "POST",
        url: server_url,
        data: JSON.stringify({
            'token': getCookie('token'),
            "command": "search_by_name",
            'max_long': max_lng,
            'min_long': min_lng,
            'max_lat': max_lat,
            'min_lat': min_lat,
            'placename': placename
        }),
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                var lat = data[i].latitude, lng = data[i].longitude;
                var url = "http://api.map.baidu.com/panorama/v2?ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb&width=1000&height=512&location=" + lng + "," + lat + "&fov=120&pitch=40&heading=90";
                var image = { "bounding_box": [], "lat": lat, "long": lng, "url": url };
                add_marker(image);
            }
            $('body').removeClass("loading");
            close_searching_window();
            //alert(data);
            //alert(obj.contry.area.women);
        },
        error: function (x) {
            $('body').removeClass("loading");
        },
        dataType: 'json'
    });

}

function display_one_image(image) {

    const draw = (ctx, x, y, w, h, score, c) => {
        ctx.beginPath();
        ctx.rect(x, y, w, h);
        ctx.strokeStyle = c;
        ctx.stroke();
        ctx.font = '15px serif';
        ctx.fillText(score, x, y - 5);
    };
    var canvas_ = jQuery('#image');
    canvas_.data("position", { lat: image.lat, long: image.long });
    var ctx = canvas_[0].getContext('2d');
    var img = new Image();
    img.crossOrigin = "Anonymous";
    bounding_boxes = image.bounding_box;
    img.onload = function () {
        ctx.drawImage(img, 0, 0);
        for (i = 0; i < bounding_boxes.length; i++) {
            [xmin, ymin, xmax, ymax, score] = bounding_boxes[i];
            draw(ctx, xmin, ymin, xmax - xmin, ymax - ymin, score, 'red');
        }
        $('#image_window, #overlay-back').fadeIn(500);
    }
    img.src = "/image/" + encodeURIComponent(image.url);
}

function add_marker(image) {
    var lat = image.lat;
    var long = image.long;
    var marker = new BMap.Marker(new BMap.Point(long, lat));
    marker.addEventListener("click", function () {
        display_one_image(image);
    });
    var removeMarker = function (e, ee, marker) {
        map.removeOverlay(marker);
    }
    var markerMenu = new BMap.ContextMenu();
    markerMenu.addItem(new BMap.MenuItem('delete', removeMarker.bind(marker)));
    marker.addContextMenu(markerMenu)
    map.addOverlay(marker);

    jQuery("#reject").unbind("click");
    (function () {
        var inner_marker = marker;
        jQuery("#reject").click(function () {
            map.removeOverlay(inner_marker);
            close_image_window();
        });
    })();
}
function display_images(images) {
    for (i = 0; i < images.length; i++) {
        (function (ii) {
            add_marker(images[ii]);
        })(i);
    }
}
