
select 标签

    HTML 内容如下:
        <select name='sele' id='sect' onchange='alert(this.options[this.selectedIndex].text)'>
            <option value='1'>第一名</option>
            <option value='2'>第二名</option>
            <option value='3'>第三名</option>
            <option value='4'>第四名</option>
        </select>

    js 使用如下:
        var select_elemet = window.document.getElementById("sect");
        var value = select_elemet.value // 这是获得选中的值
        var select_options = select_elemet.options //这是获得select中所有的值，是个数组, 里面是各 option 标签对象

        // 要获得option中间的文本
        var selectIndex = select_elemet.selectedIndex;//获得是第几个被选中了
        var selectText = select_elemet.options[selectIndex].text; //获得被选中的项目的文本
        var selectValue = select_elemet.options[selectIndex].value; //获得被选中的项目的值

        // 选中某个的 option
        var index = 0; // 要选中的 option 的下标
        select_elemet.options[index].selected = true;

        // 用 new Option("文字", "值") 方法新增 option
        select_elemet.add(new Option("4", "4"));

        // 删除所有option
        select_elemet.options.length = 0;

        // 删除选中的option
        select_elemet.options.remove(selectIndex);

        // 修改选中的option
        select_elemet.options[selectIndex] = new Option("three", 3); //更改对应的值
        select_elemet.options[selectIndex].selected = true; // 保持选中状态

        // 刪除select
        select_elemet.parentNode.removeChild(select_elemet);

    jQuery 使用如下:
        $('#mySelect').val(); //获得被选中的项目的值
        $('#mySelect option:selected').text(); //获得被选中的项目的文本

        // 选中某个的 option
        $('#mySelect').find("option[text='pxx']").attr("selected", true);

        // select选中的响应事件
		$('#mySelect').change(function(){ /*新增所需要執行的操作程式碼*/});

