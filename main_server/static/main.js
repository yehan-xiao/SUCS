//Wirtten by Shitao Tang
var server_url = "/UCS";
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function search_bounding_box() {
    $('body').addClass("loading");
    jQuery.ajax({
        type: "POST",
        url: server_url,
        data: JSON.stringify({
            'token': getCookie('token'),
            "command": "search_bounding_box",
            'max_long': max_lng,
            'min_long': min_lng,
            'max_lat': max_lat,
            'min_lat': min_lat
        }),
        success: function (data) {
            $('body').removeClass("loading");
            $("#image_analysis").removeAttr("disabled");
            alert("Find " + data + " images");
            setCookie("image_num", data);
            //alert(data);
            //alert(obj.contry.area.women);
        },
        error: function (x) {
            $('body').removeClass("loading");
            alert(x.responseText)
        },
        dataType: 'json'
    });
}

function image_analysis() {
    var object_name = jQuery('#object').find(":selected").text();
    var image_num = getCookie('image_num');
    var percent_val = '0%';
    $('#percent').text(percent_val);
    var batch = Math.max(20, image_num / 100);
    $('body').addClass("processing");
    var max_iter = image_num / batch;
    function request(i) {
        jQuery.ajax({
            type: "POST",
            url: server_url,
            data: JSON.stringify({
                "token": getCookie("token"),
                "command": "image_analysis",
                "object": object_name,
                "limit": batch
            }),
            success: function (data) {
                var percent_val = (i * 100 / max_iter).toFixed(0) + "%";
                $('#percent').text(percent_val);
                display_images(data);
                if (i < max_iter) {
                    request(i + 1);
                } else {
                    console.log(data);
                    $('body').removeClass("processing");
                    close_searching_window();
                }
            },
            error: function (x) {
            },
            dataType: 'json'

        });
    }
    request(0);
    //alert("Find " + results.length + " manhole covers")
}

blobs = [];
filenames = [];
function add_to_zip() {
    const toBlob = canvas => new Promise(resolve => canvas.toBlob(resolve));
    add_to_zip.task_item_num = add_to_zip.task_item_num || 0;
    var position = jQuery("#image").data("position");
    jQuery("#all_images").append("<tr><th>" + position.lat + "</th><th>" + position.long + "</th></tr>");
    close_image_window();
    blobs.push(toBlob($("#image")[0]));
    filenames.push("lat-" + position.lat + "-long-" + position.long + ".png");
}

function download() {

    const toBlob = canvas => new Promise(resolve => canvas.toBlob(resolve));
    const createZipWriter = () => new Promise(resolve => zip.createWriter(new zip.BlobWriter(), resolve));
    const addFile = (zipWriter, name, blob) => new Promise(resolve => zipWriter.add(name, new zip.BlobReader(blob), resolve));
    const close = zipWriter => new Promise(resolve => zipWriter.close(resolve));
    var canvas = $("#image")[0];
    var position = jQuery.data(canvas, "position");
    let zip_writer;

    if (blobs.length == 0) {
        alert("Nothing to download");
        return;
    }
    createZipWriter()
        .then(writer => {
            zip_writer = writer;
            return Promise.all(blobs);
        })
        .then(blobs => {
            const ret = [];
            let p = Promise.resolve();
            for (let i = 0; i < blobs.length; ++i) {
                p = p.then(() => {
                    return addFile(zip_writer, filenames[i], blobs[i]);
                })
                    .then(x => ret.push(x));
            }
            return p;
        })
        .then(() => {
            return close(zip_writer);
        })
        .then(x => {

            var link = document.createElement('a');
            document.body.appendChild(link);
            link.href = URL.createObjectURL(x);
            link.download = "foo.zip";
            link.click();
            filenames = [];
            blobs = [];
            jQuery("#all_images tr").remove();
            jQuery("#all_images").append("<tr><th>longitude</th><th>latitude</th></tr>")
        });

}
function change_map_engine(engine){
      jQuery.ajax({
            type: "POST",
            url: server_url,
            data: JSON.stringify({
                "token": getCookie("token"),
                "command": "change_map_engine",
                "map_engine": engine
            }),
            success: function (data) {
            },
            error: function (x) {
            },
            dataType: 'json'

        });
       
}
