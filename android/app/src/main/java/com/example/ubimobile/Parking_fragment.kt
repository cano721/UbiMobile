package com.example.ubimobile

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.parking_main.*

class Parking_fragment : Fragment {

    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.parking_main,container,false)
        return view
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        firstFloor.setOnClickListener {
            // 압력신호에서 데이터를 받으면 park 없으면 line으로 변경
            parkImg1.setImageResource(R.drawable.line1)
            parkImg2.setImageResource(R.drawable.line1)
            parkImg3.setImageResource(R.drawable.line1)
            parkImg4.setImageResource(R.drawable.park2)
            parkImg5.setImageResource(R.drawable.line2)
            parkImg6.setImageResource(R.drawable.park2)
        }
        secondFloor.setOnClickListener {
            // 압력신호에서 데이터 받으면 park 없으면 line로 변경
            parkImg1.setImageResource(R.drawable.park1)
            parkImg2.setImageResource(R.drawable.park1)
            parkImg3.setImageResource(R.drawable.park1)
            parkImg4.setImageResource(R.drawable.park2)
            parkImg5.setImageResource(R.drawable.park2)
            parkImg6.setImageResource(R.drawable.park2)
        }
    }
}