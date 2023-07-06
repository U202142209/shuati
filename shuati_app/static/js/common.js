var app = new Vue({
    el: "#adminsiteconsole",
    data: {
        code: -1,
        msg: "",
        data: [],
        tab: 1,
        addnewtagname: "",
        searchtagname: "",
        tagpage: 1,
        taglen: 10,
        // 所有的标签名字的集合
        question_data_tagnames: [],
        question_data: {
            // 用于辅助分页
            datalen: 10,
            // 选项当前的指针
            curoption: 0,
            // 选项列表
            selectoptions: [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'
            ],
        },
        // 动态添加的选项
        options: ['A', 'B', 'C', 'D', 'E'], // 初始选项
        // 用来遍历获取题目信息
        question_data_questiondata: [],
        // 当前选择的标签
        question_data_selecttagname: "",
        // 查询的关键字
        question_data_input_keywords: "",
        currentpage: 1,

    },
    methods: {
        admin_console_home() {
            this.tab = 1
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main'));
            var data = {
                "data_pie": [
                    { "value": 50, "name": "#1" },
                    { "value": 50, "name": "#2" },
                    { "value": 50, "name": "#3" },
                    { "value": 50, "name": "#4" },
                    { "value": 50, "name": "#5" }
                ]
            };
            myChart.setOption({
                title: {
                    text: '扇形图展示',
                    subtext: '测试数据',
                    left: 'center'
                },//标题
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },//鼠标移入属性
                series: [
                    {
                        name: '第一圈',
                        type: 'pie',
                        label: {
                            normal: {
                                show: false,
                            }
                        },
                        center: ['50%', '60%'],
                        radius: ['0%', '40%'],
                        data: data.data_pie
                    },
                    {
                        name: '第二圈',
                        type: 'pie',
                        radius: ['40.2%', '55%'],
                        label: {
                            normal: {
                                show: false,
                            }
                        },
                        center: ['50%', '60%'],
                        data: data.data_pie
                    },
                    {
                        name: '第三圈',//pie名称
                        type: 'pie',//形状类型
                        radius: ['55.2%', '80%'],//扇形
                        center: ['50%', '60%'],//图形位置
                        data: data.data_pie//数据源
                    }
                ]
            });
        },
        admin_console_tagadmin(intopage = 1) {
            this.tab = 2
            var tagname = this.searchtagname
            app.data = []
            app.currentpage = intopage
            $.ajax({
                url: "/shuati_app/admin_selecttag",
                dataType: "JSON",
                type: "get",
                data: {
                    tagname: tagname,
                    page: intopage
                },
                success: function (res) {
                    if (res.status) {
                        app.data = res.data
                        app.taglen = Math.ceil(res.len / 10)
                    }
                    else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    alert("系统发生了错误:" + res)
                }
            })
        },
        admin_console_addquestion() {
            this.tab = 3
            // 获取标签
            app.admin_getAllTagsName()
        },
        admin_get_questiondata(inputpage = 1) {
            app.question_data_questiondata = []
            app.currentpage = inputpage
            $.ajax({
                url: "/shuati_app/admin_select_question",
                dataType: "JSON",
                type: "get",
                data: {
                    question_content: app.question_data_input_keywords,
                    page: inputpage,
                    tagname: app.question_data_selecttagname
                },
                success: function (res) {
                    if (res.status) {
                        app.question_data_questiondata = res.data
                        app.taglen = Math.ceil(res.len / 10)
                    }
                    else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    alert("系统发生了错误:" + res)
                }
            })
        },
        admin_console_questionadmin(page = 1) {
            this.tab = 4
            // 获取标签
            app.admin_getAllTagsName()
            // 获取题目信息
            app.admin_get_questiondata(page)
        },
        admin_console_adduser() {
            this.tab = 5
        },
        admin_console_useradmin() {
            this.tab = 6
        },
        addnewtagapi() {
            var tagname = this.addnewtagname
            $.ajax({
                url: "/shuati_app/admin_addneewtag/",
                dataType: "JSON",
                type: "get",
                data: {
                    tagname: tagname
                },
                success: function (res) {
                    if (res.status) {
                        app.addnewtagname = ""
                    }
                    alert(res.msg)
                    // 更新数据源
                    app.admin_console_tagadmin(1)
                },
                error: function (res) {
                    alert("系统发生了错误:" + res)
                }
            })
        },
        deletetag(tag, nid) {
            var confirmDelete = confirm("确定要删除吗，删除后将不可恢复？");
            if (confirmDelete) {
                $.ajax({
                    url: "/shuati_app/admin_deletetag/",
                    dataType: "JSON",
                    type: "get",
                    data: {
                        tagname: tag,
                        nid: nid
                    },
                    success: function (res) {
                        if (res.status) {

                        }
                        else {
                            alert(res.msg)
                        }
                        // 刷新
                        app.admin_console_tagadmin(1)
                    },
                    error: function (res) {
                        alert("系统发生了错误:" + res)
                    }
                })
            };
        },
        edittag(tag, nid) {
            var newtagname = prompt("请输入新的题目分类标签的名称:", tag);
            $.ajax({
                url: "/shuati_app/admin_edit_tag/",
                dataType: "JSON",
                type: "get",
                data: {
                    tagname: newtagname,
                    nid: nid
                },
                success: function (res) {
                    alert(res.msg)
                    // 刷新
                    app.admin_console_tagadmin(1)
                },
                error: function (res) {
                    alert("系统发生了错误:" + res)
                }
            })
        },
        admin_getAllTagsName() {
            $.ajax({
                url: "/shuati_app/admin_getAllTagsName/",
                dataType: "JSON",
                type: "get",
                data: {},
                success: function (res) {
                    if (res.status) {
                        // 更新标签
                        app.question_data_tagnames = res.data
                    }
                    else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    alert("系统发生了错误:" + res)
                }
            })
        },
        addOption() {
            const lastOption = this.options[this.options.length - 1];
            const nextOption = String.fromCharCode(lastOption.charCodeAt(0) + 1);
            this.options.push(nextOption);
        },
        removeOption() {
            this.options.pop();
        },
        submitForm(event) {
            var confirmDelete = confirm("确定要提交表单吗，新增的题目信息提交后将不可修改，请确保输入无误");
            if (confirmDelete) {
                // 阻止表单默认提交行为
                event.preventDefault();
                // 将form表单数据打包
                var formData = $("#submitForm").serialize();
                // 发送Ajax请求
                $.ajax({
                    url: '/shuati_app/admin_add_question/',
                    method: 'GET',
                    data: formData,
                    success: function (res) {
                        // 请求成功处理逻辑
                        alert(res.msg)
                        if (res.status) {
                            // 清空表单
                            document.getElementById("submitForm").reset();
                            // 切换页面
                            app.admin_console_addquestion()
                        }
                    },
                    error: function (error) {
                        alert("系统发生了错误:" + res)
                    }
                });
            }
        },
        getQuestionById(question_id) {
            $.ajax({
                url: "/shuati_app/admin_getQuestionByNid",
                dataType: "JSON",
                type: "get",
                data: {
                    question_id: question_id
                },
                success: function (res) {
                    if (res.status) {
                        var message = "查询问题成功\n问题描述:  " + res.data["question_content"]
                        for (let key in res.data["options"]) {
                            if (res.data["options"].hasOwnProperty(key)) {
                                const value = res.data["options"][key];
                                message += "\n  " + key + ". " + value
                            }
                        }
                        message += "\n正确答案：" + res.data["correct_answer"]
                        message += "\n题目所属标签：" + res.data["tag"]
                        message += "\n答案解析：" + res.data["answer_detail"]
                        message += "\n答题人数：" + res.data["answer_num"]
                        message += "\n题目创建时间：" + res.data["create_time"]
                        message += "\n题目id：" + res.data["question_id"]
                        alert(message)
                    }
                    else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    alert("系统发生了错误:" + res)
                }
            })
        },
        admin_deleteQuestion(question_id) {
            var confirmDelete = confirm("确定要删除吗，删除后将不可恢复？");
            if (confirmDelete) {
                $.ajax({
                    url: "/shuati_app/admin_deleteQuestion",
                    dataType: "JSON",
                    type: "get",
                    data: {
                        question_id: question_id
                    },
                    success: function (res) {
                        alert(res.msg)
                        app.admin_get_questiondata()
                    },
                    error: function (res) {
                        console.log(res)
                        alert("系统发生了错误:" + res)
                    }
                })
            }
        },
    }
})


// 获取 id 为 logout 的 a 标签
const logoutLink = document.getElementById('logout');
// 添加点击事件处理程序
logoutLink.addEventListener('click', (event) => {
    // 阻止默认的页面跳转行为
    event.preventDefault();

    // 弹出确认框
    const result = confirm('确定要退出登录吗？');

    // 如果用户点击了确定按钮
    if (result) {
        // 获取目标链接
        const href = logoutLink.getAttribute('href');

        // 进行页面跳转
        window.location.href = href;
    }
});



/*当点击调用此方法后,将悬浮窗口显示出来,背景变暗*/
function displayWindow() {
    /*悬浮窗口的显示,需要将display变成block*/
    document.getElementById("window").style.display = "block";
    /*将背景变暗*/
    document.getElementById("shadow").style.display = "block";
}

/*当点击调用此方法,将悬浮窗口和背景全部隐藏*/
function hideWindow() {
    document.getElementById("window").style.display = "none";
    document.getElementById("shadow").style.display = "none";
}




