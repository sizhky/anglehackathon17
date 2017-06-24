package com.example.abiduzair.demohack;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
//import android.view.View;
//import android.widget.Button;
import android.widget.ImageView;

import java.io.File;

public class MainActivity extends AppCompatActivity {

//    Button button;
    ImageView imgView;
    static final int CAM_REQUEST = 1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
//        button = (Button) findViewById(R.id.button);
        imgView = (ImageView) findViewById(R.id.image_view);
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        File file = getFile();
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file));
        startActivityForResult(cameraIntent,CAM_REQUEST);
//        button.setOnClickListener(new View.OnClickListener(){

//            @Override
//            public void onClick(View v) {
//                Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
//                File file = getFile();
//                cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file));
//                startActivityForResult(cameraIntent,CAM_REQUEST);
//            }
//        });
    }
    @SuppressWarnings("all")
    private File getFile(){
        File folder = new File("sdcard/camera_app");
        if(!folder.exists())
            folder.mkdir();
        File imgfile = new File(folder,"cam_image.jpg");
        return imgfile;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        String path = "sdcard/camera_app/cam_image.jpg";
        imgView.setImageDrawable(Drawable.createFromPath(path));
    }
}
