import globalStyles from "../../../styles/styles.module.css";

const Dropdown = (props) => {
    function handleChange(event) {
        props.onChange(event.target.value);
    }

    return (
        <div style={{"position":"absolute", "marginTop":"-90px"}} className={globalStyles.mapContainer}>
            <div className={globalStyles.SearchContainer}>
                <div className={globalStyles.SearchBar}>
                    <input style={{"zIndex": "1"}} type="text" placeholder="" onChange={handleChange}/>
                </div>
            </div>
            <div className={globalStyles.SearchContainer}>
                <div className={globalStyles.SearchBar}>
                    {Object.keys(props.friendSuggestions).map((key, index) => 
                        <div style={{"display":"flex", "width":"100%", "flexFlow":"row wrap"}}>
                            {index===0 && (
                            <div className={globalStyles.spacer}/>
                            )}
                            <div style={{"marginTop": "0px", "zIndex": "0", "height":"108px"}} className={index%2 ? globalStyles.friendInfoHeader : globalStyles.friendInfoHeaderOdd} onClick={props.onClick(key)}>
                                <div className={globalStyles.headerContainer}>
                                <span> 
                                    <img style={{"width":"80px", "height":"80px", "zIndex":"2"}}className={globalStyles.profilePicture} src={props.friendSuggestions[key][2]}/> 
                                </span>
                                <span>
                                    <div style={{"fontSize":"24px"}} className={globalStyles.friendName}>{props.friendSuggestions[key][0]}</div>
                                    <div className={globalStyles.friendH5} style={{"justifySelf": "left"}}>{props.friendSuggestions[key][1]} Mutual Friends</div>
                                </span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dropdown;