package healthcare.ckwpjt.com.healthcare;

import android.app.ProgressDialog;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.VideoView;

public class MainActivity extends AppCompatActivity {

    final static String SAMPLE_VIDEO_URL = "http://192.168.0.21:8160";
    ProgressDialog mDialog;
    VideoView videoView;
    ImageView btnPlayPause;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        videoView = (VideoView) findViewById(R.id.videoView);
        btnPlayPause = (ImageButton)findViewById(R.id.btn_play_pause);
        btnPlayPause.setOnClickListener(onClickListener);
    }

    ImageButton.OnClickListener onClickListener = new ImageButton.OnClickListener(){

        @Override
        public void onClick(View v) {

            mDialog = new ProgressDialog(MainActivity.this);
            mDialog.setMessage("Please wait..");
            mDialog.show();

            try {

                if (!videoView.isPlaying()) {

                    Uri uri = Uri.parse(SAMPLE_VIDEO_URL);
                    videoView.setVideoURI(uri);
                    videoView.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                        @Override
                        public void onCompletion(MediaPlayer mp) {
                            btnPlayPause.setImageResource(R.drawable.ic_launcher_background);
                        }
                    });
                }
                else{
                    videoView.pause();
                    btnPlayPause.setImageResource(R.drawable.ic_launcher_foreground);
                }
            }
            catch (Exception e){

            }

            videoView.requestFocus();
            videoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
                @Override
                public void onPrepared(MediaPlayer mp) {
                    mDialog.dismiss();
                    mp.setLooping(true);
                    videoView.start();
                }
            });

        }
    };

}
