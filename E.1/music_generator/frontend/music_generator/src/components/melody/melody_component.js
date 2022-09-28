import { React, useState, useEffect } from "react";
import "./melody_component.scss"
import MidiPlayer from 'react-midi-player';
import axios from "axios";

export const Melody = (props) => {


    const [melody_b64, setMelody_b64] = useState(atob(props.data.melody_b64))
    const [music_id, setMusic_id] = useState(props.data._id)

    const DeleteSong = () => {
        axios({
            method: 'delete',
            url: 'http://127.0.0.1:8000/melody/' + music_id,
        }).then((res) => {
            // props.setMelodies(props.melodies.filter(item => item._id !== music_id))
            setMelody_b64('null')
        })
            .catch(err => console.log(err))
    }

    return (
        melody_b64 ? (
            <div className="melody_unit">
                <MidiPlayer data={melody_b64} />
                <button className="delete_btn" onClick={(DeleteSong)}>Supprimer</button>
            </div>
        ) : (<>
        </>)

    )
}
 