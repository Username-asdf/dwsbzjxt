<template>
    <div class="main">
        <Headers></Headers>
        <div style="width: 200px;float: left;">
            <el-menu default-active="1-3" class="el-menu-vertical-demo">
                <el-submenu index="1">
                    <template slot="title">
                        <i class="el-icon-location"></i>
                        <span slot="title">选项</span>
                    </template>
                    <el-menu-item-group>
                        <span slot="title">规则库</span>
						<el-menu-item style="display: none;" index="1-3"></el-menu-item>
                        <el-menu-item index="1-1" @click="goRules">规则库查看</el-menu-item>
                        <el-menu-item index="1-2" @click="dialogFormVisible = true">规则库添加</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-menu-item index="4" @click="open">
                    <i class="el-icon-setting"></i>
                    <span slot="title">设置</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content">
            <div class="box">
                <el-input
                        placeholder="请输入内容"
                        v-model="input"
                        clearable style="margin-bottom: 20px">
                </el-input>
                <el-button type="primary " round size="small" @click="add">添加</el-button>
                <el-button type="success " round size="small" @click="confirm">开始识别</el-button>
            </div>
        </div>
        <div class="tag">
            <el-tag
                    :key="tag"
                    v-for="tag in dynamicTags"
                    closable
                    :disable-transitions="false"
                    @close="handleClose(tag)" style="margin-bottom: 5px">
                {{tag}}
            </el-tag>
            <el-input
                    class="input-new-tag"
                    v-if="inputVisible"
                    v-model="inputValue"
                    ref="saveTagInput"
                    size="small"
                    @keyup.enter.native="handleInputConfirm"
                    @blur="handleInputConfirm"
            >
            </el-input>
        </div>

        <div class="">
            <el-dialog title="规则添加" :visible.sync="dialogFormVisible">
                <el-form :model="form">
                    <el-form-item label="前提" :label-width="formLabelWidth">
                        <el-input v-model="form.rules" autocomplete="off"
                                  placeholder="若存在多个前提，前提与前提之间请用中文逗号隔开"></el-input>
                    </el-form-item>
                    <el-form-item label="结论" :label-width="formLabelWidth">
                        <el-input v-model="form.result" autocomplete="off"></el-input>
                    </el-form-item>
                </el-form>
				<!-- 上传文件 -->
				<div style="width:370px;margin-left: 120px;">
					<el-upload
					  name="file"
					  drag
					  :show-file-list="false"
					  :on-success="uploadSuccess"
					  :on-error="uploadError"
					  accept=".txt"
					  action="http://127.0.0.1:5000/addfile">
					  <i class="el-icon-upload"></i>
					  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
					  <div class="el-upload__tip" slot="tip">只能上传txt文件</div>
					</el-upload>
				</div>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="addRules">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    import Headers from "./animal/headers";

    export default {
        name: "animal",
        components: {Headers},
        data() {
            return {
                // 输入信息
                input: '',
                // 标签部分数据
                // "吃肉", "有爪", "有犬齿", "眼盯前方", "有毛发", "有奶", "黄褐色", "黑色条纹"
                dynamicTags: [],
                inputVisible: false,
                inputValue: '',
                //记录数据的数组，向后端发送
                features: [],
                //弹出框
                dialogFormVisible: false,
                //存放添加信息
                form: {
                    rules: '',
                    result: '',
                    region: '1',
                },
                formLabelWidth: '120px'
            }
        },
        methods: {
			uploadSuccess(){ //文件上传成功
				this.$message({
				    message: '文件上传成功',
				    type: 'success'
				});
				this.dialogFormVisible = false;
			},
			uploadError(){ //文件上传失败
				this.$message({
				    message: '文件上传失败，请检查文件格式，稍后再试',
				    type: 'error'
				});
			},
            // 用于添加新的事实
            add() {
                let that = this;
                let input = that.input;
                //分解输入的字符串得到该点的经纬度坐标
                if (input.length > 0) {
                    // 添加新的标签
                    that.dynamicTags.push(that.input);
                    //分别添加对应的坐标
                    that.features.push(that.input);
                    that.input = "";
                } else {
                    that.$message({
                        message: '请将信息输入完整',
                        type: 'warning'
                    });
                }
            },
            // 用于提交给后端数据
            confirm() {
                let that = this
                if (that.features.length === 0) {
                    that.$message({
                        message: '你好像什么东西都没输入',
                        type: 'error'
                    });
                } else {
                    // 将该数据信息传递给后端
                    that.$axios({
                        method: 'post',
                        url: "http://127.0.0.1:5000/test",
                        data: {
                            msg: that.features
                        }
                    }).then(function (response) {
                        //输出识别结果
						var result = response.data.result
						const h = that.$createElement;
						
						var retHtml = []
						for(var i=0;i<result.length;i++){
							retHtml.push(h('p', null, result[i]))
						}
						if(result.length <= 0){
							retHtml = "没有找到结论"
						}
						that.$msgbox({
						  title: '识别结果',
						  message: h('div', null, retHtml),
						  confirmButtonText: '确定',
						  })
                    }).catch(function (error) {
                        alert(error)
                    })
                }
            },

            //取消指定的输入数据
            handleClose(tag) {
                //删除标签内容
                this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
                //删除指定的元素
                this.features.splice(this.features.indexOf(tag), 1);
            },

            //输入信息
            handleInputConfirm() {
                let inputValue = this.inputValue;
                if (inputValue) {
                    this.dynamicTags.push(inputValue);
                }
                this.inputVisible = false;
                this.inputValue = '';
            },
            //前往规则页面
            goRules() {
                this.$router.push('/rules')
            },
            //添加新的规则数据
            addRules() {
                let that = this;
                // 分成数组
                var strRules = that.form.rules;
                if (strRules.length === 0 || that.form.result.length === 0 || that.form.region.length === 0) {
                    that.$message({
                        message: '请将所有信息填写完整再确定',
                        type: 'error'
                    });
                } else {
                    that.$axios({
                        method: 'post',
                        url: "http://127.0.0.1:5000/add",
                        data: {
                            newrules: strRules,
                            newresult: that.form.result,
                            newtype: that.form.region
                        }
                    }).then(function (response) {
                        //输出识别结果
                        // console.log(response.data)
                        if (response.data.code === 200) {
                            that.dialogFormVisible = false;
                            that.$message({
                                message: '添加成功，可在规则库进行查看',
                                type: 'success'
                            });
                        }
                    }).catch(function (error) {
                        alert(error)
                    })
                }
            },
            open(){
                this.$alert('这里什么都没有', '信息', {
                    confirmButtonText: '确定',
                });
            }
        },
    }
</script>

<style lang="scss">

    body {
        background-image: url(../assets/background.jpg), linear-gradient(#D3D3D3, #D3D3D3);
        background-size: 1920px 1080px;
        /*使得背景图片固定不动*/
        background-attachment: fixed;
        background-blend-mode: darken;
    }

    .content {
        margin-top: 20px;
        width: 30%;
    }

    .box {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 450px;
        background: lightgray;
        padding: 40px;
        box-sizing: border-box;
        box-shadow: 0 15px 25px rgba(0, 0, 0, .1);
        border-radius: 10px;
        border: 1px solid #EBEEF5;
    }


    .tag {
        position: absolute;
        margin-top: 80px;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 450px;
    }

    /*标签*/
    .el-tag + .el-tag {
        margin-left: 10px;
    }

    .button-new-tag {
        margin-left: 10px;
        height: 32px;
        line-height: 30px;
        padding-top: 0;
        padding-bottom: 0;
    }

    .input-new-tag {
        width: 90px;
        margin-left: 10px;
        vertical-align: bottom;
    }


    .el-menu-vertical-demo:not(.el-menu--collapse) {
        width: 200px;
        min-height: 400px;
    }

</style>
