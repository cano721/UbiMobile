package com.example.ubimobile.classdata

import java.util.*

class ParkingFloorData(var pf_id:Int,var pf_data:Int){
    override fun toString(): String {
        return "${pf_id.toString()},${pf_data.toString()}"
    }
}