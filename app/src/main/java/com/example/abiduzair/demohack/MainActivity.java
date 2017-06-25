package com.example.abiduzair.demohack;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.Button;

import android.widget.ImageView;

import java.io.File;


@SuppressWarnings("all")
//
public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    private Button buttonChoose;
    private Button buttonUpload;
    Toolbar toolbar;

    private ImageView imageView;

    private Bitmap bitmap;

    private int PICK_IMAGE_REQUEST = 1;


    private String KEY_IMAGE = "image";
    private String KEY_NAME = "name";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        buttonChoose = (Button) findViewById(R.id.buttonChoose);
        buttonUpload = (Button) findViewById(R.id.buttonUpload);
        imageView = (ImageView) findViewById(R.id.imageView);

        buttonChoose.setOnClickListener(this);
        buttonUpload.setOnClickListener(this);
        showFileChooser();
    }

    private void showFileChooser() {
//        Intent intent = new Intent();
//        intent.setType("image/*");
//        intent.setAction(Intent.ACTION_GET_CONTENT);
//        startActivityForResult(Intent.createChooser(intent, "Select Picture"), PICK_IMAGE_REQUEST);
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        File file = getFile();
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file));
        startActivityForResult(cameraIntent, PICK_IMAGE_REQUEST);
    }

    private File getFile() {
        File folder = new File("sdcard/camera_app");
        if (!folder.exists())
            folder.mkdirs();
        File imgfile = new File(folder, "cam_image.jpg");
        return imgfile;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

//        if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && data != null && data.getData() != null) {
//            Uri filePath = data.getData();
            //   try {
            //Getting the Bitmap from Gallery
            //     String path = "/sdcard/camera_app/cam_image.jpg";
            //   imageView.setImageDrawable(Drawable.createFromPath(path));
            //} catch (Exception e) {
          //   e.printStackTrace();
            // }
            //}
            File imgFile = new  File("/storage/emulated/0/camera_app/cam_image.jpg");
            if(imgFile.exists()){
                Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
                ImageView imageView = (ImageView)findViewById(R.id.imageView);
                imageView.setImageBitmap(myBitmap);

//                uploadImage(imgFile.getAbsolutePath());

            }
//        }
    }

//    private void uploadImage(String picturePath){
//        Bitmap myBitmap = BitmapFactory.decodeFile(picturePath);
//        ImageView myImage = (ImageView) findViewById(R.id.imageView);
//        myImage.setImageBitmap(myBitmap);
//        ByteArrayOutputStream baos = new ByteArrayOutputStream();
//        byte[] imageBytes = baos.toByteArray();
//        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
//        RequestPackage rp = new RequestPackage();
//        rp.setMethod("POST");
//        rp.setUri(UPLOAD_URL);
//        rp.setSingleParam("base64",encodedImage);
//        rp.setSingleParam("ImageName","cam_image"+".jpg");
//
//        new uploadToServer().execute(rp);
//    }
//
//
//    public class uploadToServer extends AsyncTask<RequestPackage, Void,String> {
//        private ProgressDialog pd = new ProgressDialog(MainActivity.this);
//
//        protected void onPreExecute(){
//            super.onPreExecute();
//            pd.setMessage("Image Uploading!,please wait...");
//            pd.setCancelable(false);
//            pd.show();
//        }
//
//        @Override
//        protected String doInBackground(RequestPackage... params) {
//            String content = MyHttpURLConnection.getData(params[0]);
//            return content;
//        }
//
//        protected void onPostExecute(String result) {
//            super.onPostExecute(result);
//            pd.hide();
//            pd.dismiss();
//        }
//    }


    @Override
    public void onClick(View v) {
        if (v == buttonChoose) {
            showFileChooser();
        }
        if( v == buttonUpload){
            Intent uploadIntent = new Intent(MainActivity.this,UploadActivity.class);
            startActivity(uploadIntent);
        }
    }

//    public void sendImageRequest(){
//
//    }
//
//    public String getStringImage(Bitmap bmp){
//        bmp.compress(Bitmap.CompressFormat.JPEG, 100, baos);
//        byte[] imageBytes = baos.toByteArray();
//        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
//        return encodedImage;
//    }
//
//    private void uploadImage(){
//        //Showing the progress dialog
//        final ProgressDialog loading = ProgressDialog.show(this,"Uploading...","Please wait...",false,false);
//        StringRequest stringRequest = new StringRequest(Request.Method.POST, UPLOAD_URL,
//                new Response.Listener<String>() {
//                    @Override
//                    public void onResponse(String s) {
//                        //Disimissing the progress dialog
//                        loading.dismiss();
//                        //Showing toast message of the response
//                        Toast.makeText(MainActivity.this, s , Toast.LENGTH_LONG).show();
//                    }
//                },
//                new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError volleyError) {
//                        //Dismissing the progress dialog
//                        loading.dismiss();
//
//                        //Showing toast
//                        Toast.makeText(MainActivity.this, volleyError.getMessage().toString(), Toast.LENGTH_LONG).show();
//                    }
//                }){
//            @Override
//            protected Map<String, String> getParams() throws AuthFailureError {
//                //Converting Bitmap to String
//                String image = getStringImage(bitmap);
//
//                //Creating parameters
//                Map<String,String> params = new Hashtable<String, String>();
//
//                //Adding parameters
//                params.put(KEY_IMAGE, image);
//
//                //returning parameters
//                return params;
//            }
//        };
//
//        //Creating a Request Queue
//        RequestQueue requestQueue = Volley.newRequestQueue(this);
//
//        //Adding request to the queue
//        requestQueue.add(stringRequest);
//    }

}
