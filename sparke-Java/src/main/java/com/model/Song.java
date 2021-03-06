package com.model;

/**
 * Created by alikemal on 19.03.2017.
 */
public class Song {
    private String trackID;
    private String songID;
    private String songTitle;
    private String artistTitle;

    public Song(String trackID, String songID, String artistTitle, String songTitle) {
        this.trackID = trackID;
        this.songID = songID;
        this.songTitle = songTitle;
        this.artistTitle = artistTitle;
    }

    public Song() {
    }

    public String getTrackID() {
        return trackID;
    }

    public void setTrackID(String trackID) {
        this.trackID = trackID;
    }

    public String getSongID() {
        return songID;
    }

    public void setSongID(String songID) {
        this.songID = songID;
    }

    public String getSongTitle() {
        return songTitle;
    }

    public void setSongTitle(String songTitle) {
        this.songTitle = songTitle;
    }

    public String getArtistTitle() {
        return artistTitle;
    }

    public void setArtistTitle(String artistTitle) {
        this.artistTitle = artistTitle;
    }


}
