$(document).ready(function(){
    $("#services").on("change", function(){
        if (this.value == "rah")
        {
            $("#teamcity").attr("src","http://ecs-7fab4cf9.ecs.ads.autodesk.com/overview.html");
        }
        else
        {
            $("#teamcity").attr("src","http://ecs-436cd9b8.ecs.ads.autodesk.com/overview.html");
        }
    });

}
    );
