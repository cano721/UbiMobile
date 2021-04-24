package com.example.ubimobile.classdata

import java.util.*

class ParkData(var pf_id:Int, var p_id:Int, var pf_floor:Int, var pf_space: Int,
               var pf_data:Int){
    override fun toString(): String {
        return "${pf_id.toString()}, ${p_id.toString()}, ${pf_floor.toString()}, ${pf_space.toString()}, ${pf_data.toString()}"
    }
}