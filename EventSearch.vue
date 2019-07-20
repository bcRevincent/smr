
<template>
    <div class="app-container" style ="margin-top: 10px;margin-right:23px">
      <el-col  class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline="true" :model="attackinfo">
       
     <el-col>
        <el-form-item>
          <el-input style="width:140px" v-model="attackinfo.attackNum"  placeholder="攻击编号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="attackinfo.attackName"  placeholder="攻击名称"></el-input>
        </el-form-item>

        <el-form-item>
          <el-input style="width:350px" v-model="attackinfo.attackTarget"  placeholder="攻击目标"></el-input>
        </el-form-item>
     </el-col>
     <el-col>
         <el-form-item>
          <el-input v-model="attackinfo.cfj"  placeholder="判断标准"></el-input>
        </el-form-item>
     
        <el-form-item>
          <el-input type="text"  style="width:400px" v-model="attackinfo.attackStartTime" id="attackStartTime" placeholder="请输入起始时间"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" v-on:click="getUsers">查询</el-button>
        </el-form-item>
        <el-form-item >
          <el-input  type="hidden"  v-model="attackinfo.attackEndTime" id="attackEndTime" placeholder="结束时间：2019-01-01 00：00：00"></el-input>
        </el-form-item>
        </el-col>
        
      </el-form>
      
    </el-col>
      <el-col >
         <el-table :data=" attackInfoList" border height="520" style="width: 100%">
         <el-table-column prop="attackTime" label="攻击时间" width="250" align="center"></el-table-column>      
         <el-table-column prop="attackNum" label="攻击编号" width="130" align="center"></el-table-column>
        <el-table-column prop="attackName" label="攻击名称" width="250" align="center"></el-table-column>      
        <el-table-column prop="attackTarget" label="攻击目标" width="295" align="center"></el-table-column>
        <el-table-column prop="cfj" label="判定标准" width="230" align="center"></el-table-column>
        
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
      </el-col>
    </div>
</template>


<script>


import axios from "axios";
import qs from "qs";


export default {
  
  name: "EventLog",
  data() {
    return {
     
      attackInfoList: [],
      addFormReadOnly: true,
      dialogVisible: false,
      isView: true,
      total: 0,
      currentPage: 1,
      pagesize: 10,
  
      attackinfo: {
        //id: "",
        attackNum: "",
        attackName: "",
        attackTarget: "",
        attackStartTime:"",
        attackEndTime:"",
        cfj: ""
      },
     };
   },
  
  mounted: function() {
   
   
    this.loadData();
    
    this.lay();
    
  },


  methods: { 
    lay(){
      
      
      laydate.render({
        elem:'#attackStartTime',
        type:'datetime',
        range:'true',
        done:(value)=>{
          
          this.attackinfo.attackStartTime=value
        
        }
      });

    },
    
    localtime() {
    var date = new Date();
  var seperator1 = "-";
  var year = date.getFullYear();
  var month = date.getMonth() + 1;
  var strDate = date.getDate();
  if (month >= 1 && month <= 9) {
    month = "0" + month;
  }
  if (strDate >= 0 && strDate <= 9) {
    strDate = "0" + strDate;
  }
  var currentdate = year + seperator1 + month + seperator1 + strDate;
  this.attackInfo.attackStartTime=currentdate;
  this.attackInfo.attackEndTime=currentdate;
  },
    loadData(page = 1) {
     
      axios
        .post(
          "/EventLog/list",
          qs.stringify({ ...this.attackinfo, page, size: this.pagesize })
        )
        .then(result => {
          const { totalElements, content, size } = result.data;

          this.total = totalElements;
          this.pagesize = size;
          this.attackInfoList = content;
        });
    },
    getUsers() {
      var atk=this.attackinfo.attackStartTime;
       var as=atk.substr(0,19);
        var ad=atk.substr(-19);
      if(atk!=''&&as!=ad)
      {
        this.attackinfo.attackStartTime=as;
        this.attackinfo.attackEndTime=ad;
      }
      this.loadData();
    },
    handleCurrentChange(page) {
      console.log(page);
      this.loadData(page);
    },
    handleSizeChange(pagesize) {
      this.pagesize = pagesize;
    },
    // 这是一个定时器
    //定时刷新
    mounted() {
      if (this.timer) {
        clearInterval(this.timer);
      } else {
        this.timer = setInterval(() => {
          //获取数据
          // this.loadData();
          console.log('定时任务测试 ---- ')
        }, 1000);
      }
    },
    //组件销毁时清除
    destroyed() {
      clearInterval(this.timer);
    }
  }
}
</script>
