package com.example.ubimobile.classdata

import java.util.*

class UsersCarData(var uc_id:Int, var u_id:String, var uc_model:String, var uc_number:String,
                   var uc_color:String, var uc_ditance:Int, var uc_repair:String, var uc_age:String){
    override fun toString(): String {
        return "${uc_id.toString()}, $u_id, $uc_model, $uc_number, $uc_color" +
                "${uc_ditance.toString()},$uc_repair,$uc_age"
    }
}