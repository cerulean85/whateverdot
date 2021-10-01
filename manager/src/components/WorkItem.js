import React from "react";
import ProgressStateTextBox from "./ProgressStateTextBox";
import ButtonControl from "./ButtonControl";
import * as R from "../Resources";
import axios from "axios";

class WorkItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            item: props.value,
            opacity: 1.0,
            backgroundColor: '#212121',

        };
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);

        // console.log(this.state.item)
    }

    handleMouseHover() { this.setState(this.toggleHoverState); }
    handleMouseLeave() { this.setState(this.toggleLeaveState); }

    toggleHoverState(state) { return { opacity: 0.5, backgroundColor: '#323232' }; }
    toggleLeaveState(state) { return { opacity: 1.0, backgroundColor: '#212121' }; }

    play() {

        const currentState = this.state.item.current_state;
        if(currentState === 'processing') {
            alert('수집이 진행 중입니다.');
            return;
        }

        const request = async () => {
            let data = { group_id: this.state.item.group_id };
            const response = await axios.post('http://localhost:3030/resume_work', data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_PROCESSING } )
                window.location.reload();
            }
        };
        request()
    }

    pause() {

        const currentState = this.state.item.current_state;
        if(currentState !== 'processing') {
            alert('수집이 진행 상태가 아닐 때는 사용할 수 없습니다.');
            return;
        }

        const request = async () => {
            let data = { group_id: this.state.item.group_id };
            const response = await axios.post('http://localhost:3030/pause_work', data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_PAUSED } );
                window.location.reload();
            }
        };
        request()
    }

    stop() {

        const currentState = this.state.item.current_state;
        if(currentState === 'stopped') {
            return;
        }

        const request = async () => {
            let data = { group_id: this.state.item.group_id };
            const response = await axios.post('http://localhost:3030/stop_work', data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_STOPPED } )
                window.location.reload();
            }
        };
        request()
    }

    finish() {
        const request = async () => {
            let data = { group_id: this.state.item.group_id };
            const response = await axios.post('http://localhost:3030/finish_work', data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_FINISHED } )
                window.location.reload();
            }
        };
        request()
    }

    terminate() {

        const currentState = this.state.item.current_state;
        if(currentState === R.STATE_PROCESSING) {
            alert('수집이 진행 중인 작업은 제거할 수 없습니다.');
            return;
        }

        if(window.confirm('선택한 작업을 제거하시겠습니까?')) {
            const request = async () => {
                let data = {group_id: this.state.item.group_id};
                const response = await axios.post('http://localhost:3030/terminate_work', data);
                if (response.status !== 200) {
                    alert('요청한 작업을 수행할 수 없습니다.');
                } else {
                    this.setState({value: R.STATE_TERMINATED});
                    window.location.reload();
                }
            };
            request()
        }
    }
    error() { this.setState( { value: R.STATE_ERROR } ) }

    renderProgressStateTextBox() {

        // alert(this.state.item.work_state)
        return <ProgressStateTextBox
            value={this.state.item.work_state}
        />;
    }

    renderButtonProcess() {
        return <ButtonControl
            value={ R.STATE_PROCESSING }
            currentState = {this.state.item.work_state}
            groupdId = {this.state.item.work_group_no}
            onClick={()=> this.play()}
        />
    }

    // renderButtonPause() {
    //     return <ButtonControl
    //         value={R.STATE_PAUSED}
    //         currentState = {this.state.item.work_state}
    //         groupdId = {this.state.item.work_group_no}
    //         onClick={()=> this.pause()}
    //     />
    // }

    renderButtonStop() {
        return <ButtonControl
            value={R.STATE_STOPPED}
            currentState = {this.state.item.work_state}
            groupdId = {this.state.item.work_group_no}
            onClick={()=> this.stop()}
        />
    }

    // renderButtonTerminate() {
    //     return <ButtonControl
    //         value={R.STATE_TERMINATED}
    //         currentState = {this.state.item.current_state}
    //         groupdId = {this.state.item.group_id}
    //         onClick={()=> this.terminate()}
    //     />
    // }
    //
    // renderButtonFinish() {
    //     return <ButtonControl
    //         value={R.STATE_FINISHED}
    //         currentState = {this.state.item.current_state}
    //         groupdId = {this.state.item.group_id}
    //         onClick={()=> this.finish()}
    //     />
    // }



    render() {

        const secs = this.state.item.view_running_time;

        const hourNum = Math.floor(secs / 3600);
        const hourMod = secs % 3600;
        const minuteNum = Math.floor(hourMod / 60);
        const minuteMod = hourMod % 60;

        const hour   = (hourNum < 10 ? '0':'') + hourNum;
        const minute = (minuteNum < 10 ? '0':'') + minuteNum;
        const second = (minuteMod < 10 ? '0':'') + minuteMod;

        return (
        <div
            onMouseEnter={this.handleMouseHover}
            onMouseLeave={this.handleMouseLeave}
            onClick={(e) => {
                this.props.openPopup();
            }}
            style={{
                position: 'relative',
                width: '100%',
                height:130,
                backgroundColor: this.state.backgroundColor,
                borderBottom: '1px solid black',
                display: 'flex',
                cursor: 'pointer',
                }}
        >
            <div>
                <div
                    style={{
                        position: 'absolute',
                        top:'20%',
                        left: '2%',
                        display: 'flex'
                    }}>
                    {this.renderProgressStateTextBox()}
                    <div style={{ paddingTop:6, paddingLeft: 20, fontSize:16, color: '#666666' }}>
                        {/*경과:&nbsp;<label style={{color:'#ff9e01', fontSize:18}}>{hour}:{minute}:{second}</label>*/}
                        {/*&nbsp;&nbsp;/&nbsp;&nbsp;*/}
                        {/*완료:&nbsp;&nbsp;<label style={{color:'#a9d18e', fontSize:18}}>{this.state.item.current_work_count}</label>*/}
                        {/*&nbsp;건&nbsp;(총&nbsp;*/}
                        {/*<label style={{color:'#0099ff', fontSize:18}}>{this.state.item.total_work_count}</label>건)&nbsp;*/}
                    </div>
                </div>
                <div
                    style={{
                        position: 'absolute',
                        top:'58%',
                        left: '2%',
                        display: 'flex',
                        fontSize: '16pt'
                    }}>
                    {this.state.item.title}
                </div>
            </div>
            <div
                style={{
                    // float: 'right',
                    position: 'absolute',
                    top: '50%',
                    left: '86%',
                    transform: 'translate(-20%, -50%)',
                    display: 'flex',
                }}
            >
                {this.renderButtonProcess()}&nbsp;&nbsp;
                {/*{this.renderButtonPause()}&nbsp;&nbsp;*/}
                {this.renderButtonStop()}&nbsp;&nbsp;
                {/*{this.renderButtonTerminate()}*/}

            </div>


        </div>
        );
    }
}

export default WorkItem;