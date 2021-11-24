import { useEffect, useState } from "react";

import FriendBox from "./Components/FriendBox";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageFour.modules.css";

const StageFour = (props) => {
  const emptyFriendData = {
    name: '',
    mutualFriendCount: '',
    profilePictureURL: '',
    workplace: [''],
    college: [''],
    highschool: [''],
    places: [''],
    religion: [''],
    politics: ['']
  };

  const [query, changeQuery] = useState("");
  const [selectedFriend, changeSelectedFriend] = useState("danielnewman21");
  const [friendData, changeFriendData] = useState(emptyFriendData);
  const [searchFriendSuggestions, changeSearchFriendSuggestions] = useState([]);

  useEffect(() => {
    const request_body = {
      "friend_url": selectedFriend,
    }
    const getFriendData = fetch("http://localhost:5000/stage_four_friend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request_body),
    }).then(res => res.json()).then(data => {
      changeFriendData(data)
    });
  }, [selectedFriend]);

  useEffect(() => {
    const request_body = {
      "query": query,
    }
    const getFriendQuery= fetch("http://localhost:5000/stage_four_query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request_body)
    }).then(res => res.json()).then(data => {
      changeSearchFriendSuggestions(data)
    });
  }, [query]);

  return (
    <div className={globalStyles.background}>
    <div className={globalStyles.SearchContainer}>
      <div className={globalStyles.SearchBar}>
        <input type="text" placeholder="" onChange={event => changeQuery(event.target.value)} />
      </div>
    </div>
    <FriendBox friend={friendData}/>
    </div>
  );
};

export default StageFour;
