import styles from "../StageThreeStepThree.module.css"

const ColumnData = (props) => {
  const data = props.data;
  return (
    <div className={styles.ColumnDataItem}>
      {data && data.map( (entry) =>
        <span>{entry}</span>
      )}
    </div>
  );
};

export default ColumnData;
