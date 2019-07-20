<template>
  <div class="app-container" style ="margin-top: 10px;margin-right:27px">
    <el-col >
      <el-table :data="attackInfoList" border height="520" style="width: 100%">
        <el-table-column prop="attackTime" label="攻击时间" width="250" align="center"></el-table-column>
        <el-table-column prop="attackNum" label="攻击编号" width="130" align="center"></el-table-column>
        <el-table-column prop="attackName" label="攻击名称" width="250" align="center"></el-table-column>
        <el-table-column prop="attackTarget" label="攻击目标" width="300" align="center"></el-table-column>
        <el-table-column prop="cfj" label="判定标准" width="238" align="center"></el-table-column>


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
  // import { attackList } from "../api/api";
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
        // addFormData: {
        //   id: "",
        //   attackName: "",
        //   attackNum: "",
        //   attckTarget: "",
        //   attackTime: "",
        //   cfj: ""
        // },
        total: 0,
        currentPage: 1,
        pagesize: 10,
        //     rules2: {
        //       // id: [
        //       //   {
        //       //     required: true,
        //       //     message: "编号不能为空且必须为数字",
        //       //     trigger: "blur"
        //       //   }
        //       // ],
        //       attackTime: [
        //         {
        //           required: true,
        //           message: "攻击时间不能为空",
        //           trigger: "blur"
        //         }
        //       ],
        //       cfj: [
        //         {
        //           required: true,
        //           message: "判定标准不能为空",
        //           trigger: "blur"
        //         }
        //       ]
        //     },
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
      this.localtime();
      this.loadData();


      this.mounted();
    },

    methods: {
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


        var st=currentdate+" 00:00:00";
        var et=currentdate+" 23:59:59";
        this.attackinfo.attackStartTime=st;


        this.attackinfo.attackEndTime=et;





      },
      loadData(page=1) {
        //   let param = { attackInfo: this.filters };

        axios
          .post(
            "/EventLog/list",
            qs.stringify({ ...this.attackinfo, page, size: this.pagesize })
          )
          .then(result => {
            //console.log(result.data);
            const { totalElements, content, size } = result.data;
            this.total = totalElements;
            this.pagesize = size;
            this.attackInfoList = content;
          });
      },
      getUsers() {
        var a=this.attackinfo.attackStartTime;
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
            this.loadData();
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
