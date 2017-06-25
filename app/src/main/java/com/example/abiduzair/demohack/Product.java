package com.example.abiduzair.demohack;


public class Product {
    private int image;
    private String brand;
    private String price;
    private String URL;

    public Product(int image, String brand, String price,String URL) {
        this.image = image;
        this.brand = brand;
        this.price = price;
        this.URL = URL;
    }

    public int getImage() {
        return image;
    }

    public String getBrand() {
        return brand;
    }

    public String getPrice() {
        return "$"+price;
    }

    public void setImage(int image) {
        this.image = image;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getURL() {
        return URL;
    }

    public void setURL(String URL) {
        this.URL = URL;
    }
}