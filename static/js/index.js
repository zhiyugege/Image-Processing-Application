$("#saturation,#bright,#contrast").change(()=>{
    let sat_value = $("#saturation").val(),
        br_value = $("#bright").val(),
        co_value = $("#contrast").val()
    let info = {}
    info.sat_value = sat_value
    info.br_value = br_value
    info.co_value = co_value
    $.ajax({
            url: '/change',
            data: info, 
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken':csrf_token
            },
            success: function(res) {
                    $("#target").attr('src','/static/image/'+res.path+'.jpeg')
            },
            error:function(err) {
                console.log(err);
            }
        })
})

$("#seam_button").click(()=>{

    let url = "/seam_change"
    let width = $("#width").val(),
        height = $("#height").val()
    let info =  {}
    info.width = width
    info.height = height
    $.ajax({
        url: '/seam_change',
        data: info, 
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken':csrf_token
        },
        success: function(res) {
                $("#seam_img").attr('src','/static/image/'+res.path+'.jpeg')
        },
        error:function(err) {
            console.log(err);
        }
    })
    
})

 $("#dehanse").click(()=>{

    $.ajax({
        url: '/dehanse',
        data: {}, 
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken':csrf_token
        },
        success: function(res) {
                $("#dehanse_img").attr('src','/static/image/'+res.path+'.png')
        },
        error:function(err) {
            console.log(err);
        }
    })


 })