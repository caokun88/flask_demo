// 分页

function jumpto(name, current_page, page_size, total_page) {
    var jump_url = '';
    if (current_page == '?'){
        current_page = $("#input-jump").val();
    }
    current_page = parseInt(current_page);
    total_page = parseInt(total_page);
    if (current_page < 1){
        current_page = 1;
    }else if(current_page > total_page){
        current_page = total_page
    }
    if (name == 'user_list'){
        var nickname = $("#nickname>input").val();
        jump_url = '/auth/user/list/?current_page=' + current_page + '&page_size=' + page_size;
        if (nickname){
            jump_url += '&nickname=' + nickname;
        }
    }else if (name == 'order_list'){
        var start_time = $("#datetimepicker1>input").val();
        var end_time = $("#datetimepicker2>input").val();
        var project_id = $("#project_id").val();
        var keyword = $("#keyword").val();
        jump_url = '/order/list/?start_time=' + start_time + '&end_time=' + end_time +
                '&project_id=' + project_id + '&keyword=' + keyword + '&current_page=' + current_page +
            '&page_size=' + page_size;
    }
    if (jump_url){
        window.location.href = jump_url;
    }
}