import streamlit as st
from utils.streamlit_temp_auth import check_st_authentication

check_st_authentication()

for row in range(num_rows):
    expander = st.expander(f"Phase {row+1}", expanded=False, icon=None, width="stretch")
    with expander:
        cols = st.columns(4)
        week_index_start = row * 4
        count = 0
        for col in cols:
            with col:
                st.header(f"Week {week_index_start + count + 1}")
                for day in range(days):
                    st.subheader(f"Day {day + 1}")

                    movements = program["weeks"][f"week_{week_index_start + count + 1}"][f"day_{day + 1}"]["movements"]

                    for movement_index, movement in enumerate(movements):
                        st.markdown(f"**{movement["Name"]}**")
                        table = []
                        for set_index, set in enumerate(movement["sets"], start=1):
                            table.append({
                                "Set": set_index,
                                "Rep Range": f"{set["Reps_Target"][0]} - {set["Reps_Target"][1]}",
                                "Weight" : set["Weight"],
                                "Reps": set["Reps_Completed"]
                            })   
                        df = pd.DataFrame(table)
                        num_rows_df = len(df)
                        row_height = 35  # Approximate height per row in pixels
                        total_height = row_height * num_rows_df + 40  # Additional space for header
                        edited_df = st.data_editor(df,
                                                key=f"week{week_index_start + count + 1}_day{day+1}_movement{movement_index}",
                                                hide_index=True,
                                                use_container_width=True,
                                                height=total_height
                                                )

                        for _, row in edited_df.iterrows():
                            set_number = row["Set"]
                            set_index = int(set_number) - 1
                            movement["sets"][set_index]["Reps_Completed"] = row["Reps"]
                            movement["sets"][set_index]["Weight"] = row["Weight"]
                        doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
                        doc_ref.set(program)
            count += 1