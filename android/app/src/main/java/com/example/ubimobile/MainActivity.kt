package com.example.ubimobile

import android.os.Bundle
import android.util.Log
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter
import com.example.ubimobile.classdata.ParkingFloor
import com.example.ubimobile.classdata.User_Parcelable
import com.example.ubimobile.fragment.*
import com.google.android.material.tabs.TabLayoutMediator
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : FragmentActivity(){

    val driving_view = DriveCamFragment()


    val function_view = function_fragment()
    val setting_view = setting_fragment()
    val parking_view = Parking_fragment()
    val more_view = Driving_fragment()
    var fragmentList = ArrayList<Fragment>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        Log.d("msg","메인진입")
        var objintent = intent
        var obj = objintent.getParcelableExtra<User_Parcelable>("myobj")
        var u_id = obj?.u_id
        Log.d("msg","인텐트뽑아오기$u_id")
//        val driving_tab = findViewById<TabItem>(R.id.driving_tab)
//        val function_tab = findViewById<TabItem>(R.id.function_tab)
//        val car_setting_tab = findViewById<TabItem>(R.id.car_setting_tab)
//        val parking_tab = findViewById<TabItem>(R.id.parking_tab)



        fragmentList.add(driving_view)
        fragmentList.add(function_view)
        fragmentList.add(setting_view)
        fragmentList.add(parking_view)
        fragmentList.add(more_view)
        Log.d("msg","번들만들기")
        var bundle = Bundle()
        bundle.putString("u_id",u_id)
        parking_view.arguments = bundle
        Log.d("msg","번들만들기완료${parking_view.arguments}")

//        fragmentList.add(driving_view)
//        fragmentList.add(driving_view)
//        fragmentList.add(driving_view)

        val adapter = object : FragmentStateAdapter(this) {
            override fun getItemCount(): Int {
                return fragmentList.size
            }

            override fun createFragment(position: Int): Fragment {
                return fragmentList[position]
            }

        }
        viewPager2.adapter = adapter

        TabLayoutMediator(tabs, viewPager2) { tab, position ->
            when (position) {
                0 -> {
                    tab.text = "주행화면"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.drivig_icon);
                }
                1 -> {
                    tab.text = "기능"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.function_icon);
                }
                2 -> {
                    tab.text = "차량관리"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.car_setting_icon);
                }
                3 -> {
                    tab.text = "주차"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.parking_icon);
                }
                4 -> {
                    tab.text = "더보기"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.more_icon);
                }
            }
        }.attach()
    }
}