$(document).ready(function(){
    $(".image-zone" ).sortable();
    $("#pro-image").on('change', function(){
        readImage();
    });
});

function readImage(){
    if(window.File && window.FileReader && window.FileList && window.Blob){
        var fileList = event.target.files;
        var info = "";
        for(var i = 0; i < fileList.length; i++){
            info += "name: " + fileList[i].name + "\n" +
                    "type: " + fileList[i].type + "\n" +
                    "size: " + fileList[i].size + "\n"
            if(!fileList[i].type.match('image')){
                continue;
            }
            var reader = new FileReader();
            reader.addEventListener('load', function(event){
                $(".image-zone").append(
                    '<img class="image" src="' + event.target.result + '" />'
                )
            });
            reader.readAsDataURL(fileList[i]);
        }
        $("#pro-image").val('');
        alert(info);
    }
}