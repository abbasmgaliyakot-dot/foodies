import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { UtensilsCrossed } from 'lucide-react';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const result = await login(username, password);
    
    if (result.success) {
      toast.success('Login successful!');
      navigate('/');
    } else {
      toast.error(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'linear-gradient(135deg, #FFF1EE 0%, #F8F9FA 100%)' }}>
      <Card className="w-full max-w-md border-slate-200 shadow-lg">
        <CardHeader className="text-center space-y-4">
          <div className="flex justify-center">
            <img 
              src="https://customer-assets.emergentagent.com/job_dine-orders-1/artifacts/wkjm3b6v_IMG_6175.jpeg" 
              alt="Foodies Junction Logo" 
              className="w-32 h-32 object-contain"
            />
          </div>
          <div>
            <CardTitle className="text-3xl font-bold" style={{ fontFamily: 'DM Sans, sans-serif' }}>Foodies Junction</CardTitle>
            <CardDescription className="text-slate-600 mt-2">Sign in to manage your restaurant</CardDescription>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4" data-testid="login-form">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="border-slate-200 focus:border-[#E14D2A] focus:ring-[#E14D2A]"
                data-testid="username-input"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="border-slate-200 focus:border-[#E14D2A] focus:ring-[#E14D2A]"
                data-testid="password-input"
              />
            </div>
            <Button
              type="submit"
              className="w-full bg-[#E14D2A] hover:bg-[#C24123] text-white rounded-full font-medium"
              disabled={loading}
              data-testid="login-button"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;
