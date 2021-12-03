import { useEffect, useState } from "react";

import FriendBox from "./Components/FriendBox";
import Dropdown from "./Components/Dropdown";

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

  const [query, changeQuery] = useState("Type Name Here");
  const [selectedFriend, changeSelectedFriend] = useState("bobby.smart.775");
  const [friendData, changeFriendData] = useState(emptyFriendData);
  const [searchFriendSuggestions, changeSearchFriendSuggestions] = useState([]);

  useEffect(() => {
    const request_body = {
      "friend_url": selectedFriend,
    }
    const url = "http://localhost:5000/stage_four_friend?friend_url=" + encodeURIComponent(selectedFriend);
    const getFriendData = fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      // body: JSON.stringify(request_body),
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

  function handleChange(newValue) {
    changeQuery(newValue);
  }

  const onClickChangeSelected = (newUrl) => {
    changeSelectedFriend(newUrl)
  }

  return (
    <div className={globalStyles.background}>
    <Dropdown onChange={handleChange} friendSuggestions={searchFriendSuggestions} onClick={onClickChangeSelected}/>
    <FriendBox friend={friendData}/>
    </div>
  );
};

export default StageFour;
