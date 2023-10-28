import React, { Component } from "react";
import { render } from "react-dom";
import FilterListPage from "./FilterListPage";


export default class Portal extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <FilterListPage />
            </div>
        );
    }
}

const portalDiv = document.getElementById("portal");
render(<Portal />, portalDiv); 
