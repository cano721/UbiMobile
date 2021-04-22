package com.example.ubimobile.classdata

import android.os.Parcel
import android.os.Parcelable

//안드로이드에서는 객체를 인텐트에 공유하고 싶으면 Parcelable타입으로 정의
//자동으로 메소드가 오버라이딩되고 생성자가 추가
class ParkingFloor() : Parcelable {
    var pf_id:String? = ""
    var pf_data:String? = ""

    constructor(parcel: Parcel) : this() {
        pf_id = parcel.readString()
        pf_data = parcel.readString()
    }

    override fun writeToParcel(parcel: Parcel, flags: Int) {
        parcel.writeString(pf_id)
        parcel.writeString(pf_data)
    }

    override fun describeContents(): Int {
        return 0
    }

    companion object CREATOR : Parcelable.Creator<ParkingFloor> {
        override fun createFromParcel(parcel: Parcel): ParkingFloor {
           val obj = ParkingFloor()
            obj.pf_id = parcel.readString()
            obj.pf_data = parcel.readString()
            return obj
        }

        override fun newArray(size: Int): Array<ParkingFloor?> {
            return arrayOfNulls(size)
        }
    }
}