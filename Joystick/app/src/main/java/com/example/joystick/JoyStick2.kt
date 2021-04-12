/*
package com.example.joystick

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Paint
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
const val STICK_NONE = 0
const val STICK_UP = 1
const val STICK_UPRIGHT = 2
const val STICK_RIGHT = 3
const val STICK_DOWNRIGHT = 4
const val STICK_DOWN = 5
const val STICK_DOWNLEFT = 6
const val STICK_LEFT = 7
const val STICK_UPLEFT = 8
var stick_width = 0;
var stick_height:Int = 0
var STICK_ALPHA = 200
var LAYOUT_ALPHA = 200
var OFFSET = 0
var paint: Paint? = null
var stick: Bitmap? = null
var mContext: Context? = null
var mLayout: ViewGroup? = null
var params: ViewGroup.LayoutParams? = null
var position_x =0;
var position_y:Int = 0;
var min_distance:Int = 0
var distance = 0f;
var angle:kotlin.Float = 0f
var touch_state = false
var draw: JoyStick2.DrawCanvas? = null

class JoyStick2 {




    fun JoyStick(
        context: Context?,
        layout: ViewGroup?,
        stick_res_id: Int
    ) {
        mContext = context
        stick = BitmapFactory.decodeResource(mContext!!.resources, stick_res_id)
        stick_width = stick.getWidth()
        stick_height = stick.getHeight()
        draw = DrawCanvas(mContext)
        paint = Paint()
        mLayout = layout
        params = mLayout!!.layoutParams
    }

    fun drawStick(arg1: MotionEvent) {
        position_x = (arg1.x - params!!.width / 2).toInt()
        position_y = (arg1.y - params!!.height / 2).toInt()
        distance = Math.sqrt(
            Math.pow(
                position_x.toDouble(),
                2.0
            ) + Math.pow(
                position_y.toDouble(),
                2.0
            )
        ).toFloat()
        angle = cal_angle(position_x.toFloat(), position_y.toFloat()).toFloat()
        if (arg1.action == MotionEvent.ACTION_DOWN) {
            if (distance <= params!!.width / 2 - OFFSET) {
                draw!!.position(arg1.x, arg1.y)
                draw()
                touch_state = true
            }
        } else if (arg1.action == MotionEvent.ACTION_MOVE && touch_state) {
            if (distance <= params!!.width / 2 - OFFSET) {
                draw!!.position(arg1.x, arg1.y)
                draw()
            } else if (distance > params!!.width / 2 - OFFSET) {
                var x = (Math.cos(
                    Math.toRadians(
                        cal_angle(
                            position_x.toFloat(),
                            position_y.toFloat()
                        )
                    )
                )
                        * (params!!.width / 2 - OFFSET)).toFloat()
                var y = (Math.sin(
                    Math.toRadians(
                        cal_angle(
                            position_x.toFloat(),
                            position_y.toFloat()
                        )
                    )
                )
                        * (params!!.height / 2 - OFFSET)).toFloat()
                x += (params!!.width / 2).toFloat()
                y += (params!!.height / 2).toFloat()
                draw!!.position(x, y)
                draw()
            } else {
                mLayout!!.removeView(draw)
            }
        } else if (arg1.action == MotionEvent.ACTION_UP) {
            mLayout!!.removeView(draw)
            touch_state = false
        }
    }

    fun getPosition(): IntArray? {
        return if (distance > min_distance && touch_state) {
            intArrayOf(position_x, position_y)
        } else intArrayOf(0, 0)
    }

    fun getX(): Int {
        return if (distance > min_distance && touch_state) {
            position_x
        } else 0
    }

    fun getY(): Int {
        return if (distance > min_distance && touch_state) {
            position_y
        } else 0
    }

    fun getAngle(): Float {
        return if (distance > min_distance && touch_state) {
            angle
        } else 0
    }

    fun getDistance(): Float {
        return if (distance > min_distance && touch_state) {
            distance
        } else 0
    }

    fun setMinimumDistance(minDistance: Int) {
        min_distance = minDistance
    }

    fun getMinimumDistance(): Int {
        return min_distance
    }

    fun get8Direction(): Int {
        if (distance > min_distance && touch_state) {
            if (angle >= 247.5 && angle < 292.5) {
                return STICK_UP
            } else if (angle >= 292.5 && angle < 337.5) {
                return STICK_UPRIGHT
            } else if (angle >= 337.5 || angle < 22.5) {
                return STICK_RIGHT
            } else if (angle >= 22.5 && angle < 67.5) {
                return STICK_DOWNRIGHT
            } else if (angle >= 67.5 && angle < 112.5) {
                return STICK_DOWN
            } else if (angle >= 112.5 && angle < 157.5) {
                return STICK_DOWNLEFT
            } else if (angle >= 157.5 && angle < 202.5) {
                return STICK_LEFT
            } else if (angle >= 202.5 && angle < 247.5) {
                return STICK_UPLEFT
            }
        } else if (distance <= min_distance && touch_state) {
            return STICK_NONE
        }
        return 0
    }

    fun get4Direction(): Int {
        if (distance > min_distance && touch_state) {
            if (angle >= 225 && angle < 315) {
                return STICK_UP
            } else if (angle >= 315 || angle < 45) {
                return STICK_RIGHT
            } else if (angle >= 45 && angle < 135) {
                return STICK_DOWN
            } else if (angle >= 135 && angle < 225) {
                return STICK_LEFT
            }
        } else if (distance <= min_distance && touch_state) {
            return STICK_NONE
        }
        return 0
    }

    fun setOffset(offset: Int) {
        OFFSET = offset
    }

    fun getOffset(): Int {
        return OFFSET
    }

    fun setStickAlpha(alpha: Int) {
        STICK_ALPHA = alpha
        paint!!.alpha = alpha
    }

    fun getStickAlpha(): Int {
        return STICK_ALPHA
    }

    fun setLayoutAlpha(alpha: Int) {
        LAYOUT_ALPHA = alpha
        mLayout!!.background.alpha = alpha
    }

    fun getLayoutAlpha(): Int {
        return LAYOUT_ALPHA
    }

    fun setStickSize(width: Int, height: Int) {
        stick = Bitmap.createScaledBitmap(stick!!, width, height, false)
        stick_width = stick.getWidth()
        stick_height = stick.getHeight()
    }

    fun setStickWidth(width: Int) {
        stick = Bitmap.createScaledBitmap(stick!!, width, stick_height, false)
        stick_width = stick.getWidth()
    }

    fun setStickHeight(height: Int) {
        stick = Bitmap.createScaledBitmap(stick!!, stick_width, height, false)
        stick_height = stick.getHeight()
    }

    fun getStickWidth(): Int {
        return stick_width
    }

    fun getStickHeight(): Int {
        return stick_height
    }

    fun setLayoutSize(width: Int, height: Int) {
        params!!.width = width
        params!!.height = height
    }

    fun getLayoutWidth(): Int {
        return params!!.width
    }

    fun getLayoutHeight(): Int {
        return params!!.height
    }

    private fun cal_angle(x: Float, y: Float): Double {
        if (x >= 0 && y >= 0) return Math.toDegrees(Math.atan(y / x.toDouble())) else if (x < 0 && y >= 0) return Math.toDegrees(
            Math.atan(y / x.toDouble())
        ) + 180 else if (x < 0 && y < 0) return Math.toDegrees(Math.atan(y / x.toDouble())) + 180 else if (x >= 0 && y < 0) return Math.toDegrees(
            Math.atan(y / x.toDouble())
        ) + 360
        return 0.0
    }

    private fun draw() {
        try {
            mLayout!!.removeView(draw)
        } catch (e: Exception) {
        }
        mLayout!!.addView(draw)
    }

    class DrawCanvas constructor(mContext: Context?) :
        View(mContext) {
        var x : Float = 0.0f;
        var y:Float = 0.0f;
        public override fun onDraw(canvas: Canvas) {
            canvas.drawBitmap(stick, x, y, paint)
        }

        fun position(pos_x: Float, pos_y: Float) {
            x = pos_x - stick_width / 2
            y = pos_y - stick_height / 2
        }
    }
}*/
