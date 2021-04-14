/*
package com.example.joystick

import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.view.View.OnTouchListener
import android.widget.RelativeLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.joystick.*

class MainActivity2 : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.joystick);
       */
/* textView1 = findViewById<View>(R.id.textView1) as TextView
        textView2 = findViewById<View>(R.id.textView2) as TextView
        textView3 = findViewById<View>(R.id.textView3) as TextView
        textView4 = findViewById<View>(R.id.textView4) as TextView
        textView5 = findViewById<View>(R.id.textView5) as TextView*//*

*/
/**//*

        layout_joystick = findViewById<View>(R.id.layout_joystick) as RelativeLayout

        js = JoyStick(applicationContext, layout_joystick, R.drawable.pink_ball)
        js.setStickSize(150, 150)
        js.setLayoutSize(500, 500)
        js.setLayoutAlpha(150)
        js.setStickAlpha(100)
        js.setOffset(90)
        js.setMinimumDistance(50)

        layout_joystick.setOnTouchListener(OnTouchListener { arg0, arg1 ->
            js.drawStick(arg1)
            if (arg1.action == MotionEvent.ACTION_DOWN
                    || arg1.action == MotionEvent.ACTION_MOVE) {
                textView1.setText("X : " + js.getX().toString())
                textView2.setText("Y : " + js.getY().toString())
                textView3.setText("Angle : " + js.getAngle().toString())
                textView4.setText("Distance : " + js.getDistance().toString())
                val direction: Int = js.get8Direction()
                if (direction == JoyStick.STICK_UP) {
                    textView5.setText("Direction : Up")
                } else if (direction == JoyStick.STICK_UPRIGHT) {
                    textView5.setText("Direction : Up Right")
                } else if (direction == JoyStick.STICK_RIGHT) {
                    textView5.setText("Direction : Right")
                } else if (direction == JoyStick.STICK_DOWNRIGHT) {
                    textView5.setText("Direction : Down Right")
                } else if (direction == JoyStick.STICK_DOWN) {
                    textView5.setText("Direction : Down")
                } else if (direction == JoyStick.STICK_DOWNLEFT) {
                    textView5.setText("Direction : Down Left")
                } else if (direction == JoyStick.STICK_LEFT) {
                    textView5.setText("Direction : Left")
                } else if (direction == JoyStick.STICK_UPLEFT) {
                    textView5.setText("Direction : Up Left")
                } else if (direction == JoyStick.STICK_NONE) {
                    textView5.setText("Direction : Center")
                }
            } else if (arg1.action == MotionEvent.ACTION_UP) {
                textView1.setText("X :")
                textView2.setText("Y :")
                textView3.setText("Angle :")
                textView4.setText("Distance :")
                textView5.setText("Direction :")
            }
            true
        })
    }
}*/
