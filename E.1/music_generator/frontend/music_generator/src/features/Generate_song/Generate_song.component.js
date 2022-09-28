import { React, useEffect, useState } from "react";
import './Generate_song.component.scss';
import axios from "axios";
import MidiPlayer from 'react-midi-player';

import { Melody } from "../../components/melody/melody_component";

export const GenerateSong = (props) => {


    const [song, setSong] = useState();
    const [b64Format, setB64Format] = useState(null);
    const [speedFactor, setSpeedFactor] = useState(1);
    const [file, setFile] = useState(null)

    const [isLoading, setIsLoading] = useState(false)

    // const setValues = (e) => {



    // }

    const SendGeneration = () => {
        setIsLoading(true)
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            setB64Format(reader.result)
        }
        axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/generateSong/',
            data: {
                value: b64Format,
                speedFactor: speedFactor
            }
        })
            .then(async (res) => {
                let atobed = atob(res.data);
                setSong(atobed)
                setIsLoading(false)
                setSpeedFactor(1)
                setB64Format(null)
            })
            .catch(err => setSong(null))
    }
    useEffect( () => {
    }, [song])

    return (
        <>
            <div className="music_form">
            <label htmlFor='file' className="label_file">MIDI file</label>
                <input
                    className="input_file"
                    type='file'
                    onChange={(e) => setFile(e.target.files[0])}
                    name='file'
                    id='file'
                />
                
                <label className="label_speed">Echelle de vitesse</label>
                <input
                className="input_speed"
                    type='number'
                    value={speedFactor}
                    onChange={(e) => setSpeedFactor(e.target.value)}
                />
                <button className="generation_btn" onClick={SendGeneration}>Générer</button>
                {isLoading ? (<div className="loading">Chargement ...</div>) : (<></>)}
                {/* {song ? (<MidiPlayer loop={true} data={song} />) : (<></>)} */}
            </div>
        </>
    )
}