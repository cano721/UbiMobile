package com.example.ubimobile.fragment

import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.ubimobile.R
import kotlinx.android.synthetic.main.fragment_drive_cam.*

class DriveCamFragment : Fragment() {
    override fun onAttach(context: Context) {
        super.onAttach(context)
        Log.d("lifecycle","Fragment:::::::DriveCam_onAttach()")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("lifecycle","Fragment:::::::DriveCam_onCreate()")
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d("lifecycle","Fragment:::::::DriveCam_onCreateView()")
        val view = inflater.inflate(R.layout.fragment_drive_cam,container,false)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        web_view_cam.loadUrl("http://192.168.200.127:8088")
        Log.d("lifecycle","Fragment:::::::DriveCam_onViewCreated()")
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        Log.d("lifecycle","Fragment:::::::DriveCam_onActivityCreated()")
    }

    override fun onStart() {
        super.onStart()
        Log.d("lifecycle","Fragment:::::::DriveCam_onStart()")
    }

    override fun onResume() {
        super.onResume()
        Log.d("lifecycle","Fragment:::::::DriveCam_onResume()")
    }

    override fun onPause() {
        super.onPause()
        Log.d("lifecycle","Fragment:::::::DriveCam_onPause()")
    }

    override fun onStop() {
        super.onStop()
        Log.d("lifecycle","Fragment:::::::DriveCam_onStop()")
    }

    override fun onDestroyView() {
        super.onDestroyView()
        Log.d("lifecycle","Fragment:::::::DriveCam_onDestroyView()")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("lifecycle","Fragment:::::::DriveCam_onDestroy()")
    }

    override fun onDetach() {
        super.onDetach()
        Log.d("lifecycle","Fragment:::::::DriveCam_onDetach()")
    }
}