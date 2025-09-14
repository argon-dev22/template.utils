import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // サーバーからタスク一覧を取得
  const fetchTasks = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('/api/tasks');
      setTasks(response.data);
    } catch (err) {
      setError('タスクの取得に失敗しました: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 新しいタスクを追加
  const addTask = async (e) => {
    e.preventDefault();
    if (!newTask.title.trim()) {
      setError('タイトルは必須です');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await axios.post('/api/tasks', newTask);
      setTasks([...tasks, response.data]);
      setNewTask({ title: '', description: '' });
    } catch (err) {
      setError('タスクの追加に失敗しました: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // タスクを削除
  const deleteTask = async (taskId) => {
    setLoading(true);
    setError('');
    try {
      await axios.delete(`/api/tasks/${taskId}`);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('タスクの削除に失敗しました: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // コンポーネント初期化時にタスクを取得
  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="container">
      <div className="header">
        <h1>📋 Template Utils - タスク管理アプリ</h1>
        <p>React + Python + PostgreSQLのサンプルアプリケーション</p>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <h2>新しいタスクを追加</h2>
        <form onSubmit={addTask}>
          <div className="form-group">
            <label htmlFor="title">タイトル</label>
            <input
              type="text"
              id="title"
              value={newTask.title}
              onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
              placeholder="タスクのタイトルを入力してください"
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">説明</label>
            <textarea
              id="description"
              rows="3"
              value={newTask.description}
              onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
              placeholder="タスクの詳細説明（任意）"
              disabled={loading}
            />
          </div>
          <button type="submit" className="btn" disabled={loading}>
            {loading ? '追加中...' : 'タスクを追加'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2>タスク一覧 ({tasks.length}件)</h2>
        {loading && <div className="loading">読み込み中...</div>}

        {tasks.length === 0 && !loading ? (
          <p>まだタスクがありません。上のフォームから新しいタスクを追加してください。</p>
        ) : (
          <div>
            {tasks.map((task) => (
              <div key={task.id} className="task-item">
                <h3>{task.title}</h3>
                {task.description && <p>{task.description}</p>}
                <small>作成日時: {new Date(task.created_at).toLocaleString('ja-JP')}</small>
                <br />
                <button
                  onClick={() => deleteTask(task.id)}
                  className="btn"
                  style={{ backgroundColor: '#dc3545', marginTop: '10px' }}
                  disabled={loading}
                >
                  削除
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
