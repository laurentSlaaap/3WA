import {React, useState, useEffect} from "react";
import "./melodies.scss"
import axios from "axios";


import { Melody } from "../../components/melody/melody_component";

export const Melodies = (props) => {

    const [melodies, setMelodies] = useState([]);

    useEffect( () => {
        axios.get("http://127.0.0.1:8000/melodies/")
        .then(res => setMelodies(res.data))

    }, [])

    useEffect( () => {
        !melodies ? (
            window.location.reload()
    ) : (<></>)
        
    }, [melodies])

    return (
        <>
        <div className="all_melodies">
            <h2>Mélodies générées</h2>
            
            {melodies.length > 0 ? (melodies.map( (element, index) => <Melody key={index} className="melody_unit" data={element} setMelodies={setMelodies}  melodies={melodies}/>)) : (<>Chargement</>) }
        </div>
        </>
    )
}