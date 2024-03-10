<template>
    <div class="">
        <Headers></Headers>
        <div class="content">
			<el-table
			border
			    :data="rules"
			    style="width: 100%"
				stripe
			    max-height="600">
			    <el-table-column
				type="index"
			      label="ID"
			      width="50">
			    </el-table-column>
			    <el-table-column
			      label="前提"
			      width="450">
				  <template slot-scope="scope1">
				    {{scope1.row.name.join(" - ")}}
				  </template>
			    </el-table-column>
				<el-table-column
				  prop="result"
				  label="结论"
				  width="200">
				</el-table-column>
			    <el-table-column
			      fixed="right"
			      label="操作"
			      width="120">
			      <template slot-scope="scope">
			        <el-button
			          @click.native.prevent="deleteRow(scope.$index, rules)"
			          type="text"
			          size="small">
			          移除
			        </el-button>
					
			      </template>
			    </el-table-column>
			  </el-table>
        </div>
    </div>
</template>

<script>
    import Headers from "./headers";
	

    export default {
        name: "rules",
        components: {Headers},
        data() {
            return {
                result: [],
                rules: []
            }
        },
		methods:{
			deleteRow(index, data){
				
				var that = this
				
				this.$axios({
				    method: 'post',
				    url: "http://127.0.0.1:5000/delrow",
					data: {'rules':this.rules[index]}
				}).then(function (response) {
				    console.log(response.data)
				    let data = response.data
					if(data.code == 200){
						that.$message({
						  message: '删除成功',
						  type: 'success'
						});
					that.rules.splice(index, 1);
					}else{
						that.$message.error('删除失败，请稍后再试');
					}
					
				}).catch(function (error) {
				    console.log(error)
					that.$message.error('服务器正忙，请稍后再试');
				})
			}
		},
        // 在模板渲染成html后调用，通常是初始化页面完成后，再对html的dom节点进行一些需要的操作。
        mounted() {
            let that = this;
            // 将该数据信息传递给后端
            that.$axios({
                method: 'post',
                url: "http://127.0.0.1:5000/getrules",
            }).then(function (response) {
                console.log(response.data)
                let data = response.data
                that.result = data.result
				
				var rules = []
				for(var i=0;i<data.rules.length;i++){
					var temp = {}
					temp.id = i+1
					temp.name = data.rules[i]
					temp.result = data.result[i]
					rules.push(temp)
				}
                that.rules =rules 
            }).catch(function (error) {
                console.log(error)
            })
        }
    }
</script>

<style scoped>
    .content {
        margin: 0 auto;
        width: 60%;
        margin-top: 30px;

    }

    li {
        font-weight: bold;
        text-align: center;
    }
</style>
