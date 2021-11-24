import globalStyles from "../../../styles/styles.module.css";

const Dropdown = (props) => {
    function handleChange(event) {
        props.onChange(event.target.value);
    }

    return (
        <div>
            <div className={globalStyles.SearchContainer}>
                <div className={globalStyles.SearchBar}>
                    <input style={{"zIndex": "1"}} type="text" placeholder="" onChange={handleChange}/>
                </div>
            </div>
            <div className={globalStyles.SearchContainer}>
                <div className={globalStyles.SearchBar}>
                    {Object.keys(props.friendSuggestions).map((key, index) => 
                        <div style={{"marginTop": "-20px", "zIndex": "0"}} className={index%2 ? globalStyles.friendInfoHeaderEven : globalStyles.friendInfoHeader} onClick={props.onClick(key)}>
                            <div className={globalStyles.headerContainer}>
                            <span> 
                                <img className={globalStyles.profilePicture} src={props.friendSuggestions[key][2]}/> 
                            </span>
                            <span>
                                <div className={globalStyles.friendName}>{props.friendSuggestions[key][0]}</div>
                                <div className={globalStyles.friendH4} style={{"justifySelf": "left"}}>{props.friendSuggestions[key][1]} Mutual Friends</div>
                            </span>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dropdown;