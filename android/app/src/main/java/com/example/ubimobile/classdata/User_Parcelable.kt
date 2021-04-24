package com.example.ubimobile.classdata

import android.os.Parcel
import android.os.Parcelable

//안드로이드에서는 객체를 인텐트에 공유하고 싶으면 Parcelable타입으로 정의
//자동으로 메소드가 오버라이딩되고 생성자가 추가
class User_Parcelable() : Parcelable {
    var u_id:String? = ""
    var u_name:String? = ""

    constructor(parcel: Parcel) : this() {
        u_id = parcel.readString()
        u_name = parcel.readString()
    }

    override fun writeToParcel(parcel: Parcel, flags: Int) {
        parcel.writeString(u_id)
        parcel.writeString(u_name)
    }

    override fun describeContents(): Int {
        return 0
    }

    companion object CREATOR : Parcelable.Creator<User_Parcelable> {
        override fun createFromParcel(parcel: Parcel): User_Parcelable {
           val obj = User_Parcelable()
            obj.u_id = parcel.readString()
            obj.u_name = parcel.readString()
            return obj
        }

        override fun newArray(size: Int): Array<User_Parcelable?> {
            return arrayOfNulls(size)
        }
    }
}